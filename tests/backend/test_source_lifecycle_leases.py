"""Deterministic SL-13 regressions; no wall-clock sleeps or TTL policy changes."""
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import pytest

from backend.app.services.document_storage import DocumentStorage


@pytest.fixture
def source(tmp_path):
    removed = []
    storage = DocumentStorage(tmp_path, ttl_seconds=10, max_upload_bytes=1024,
                              read_chunk_bytes=32, on_removed=removed.append)
    identity = storage.allocate_id()
    path = storage.path_for(identity)
    path.write_bytes(b"synthetic source")
    os.utime(path, (100, 100))
    return storage, identity, path, removed


@pytest.mark.parametrize("operation", ["delete", "sweep"])
def test_inner_exit_does_not_release_outer_protection(source, operation):
    storage, identity, path, removed = source
    with storage.lease(identity):
        with storage.lease(identity):
            assert path.read_bytes() == b"synthetic source"
        if operation == "delete":
            assert storage.delete(identity) is False
        else:
            assert storage.sweep_expired(now=111) == []
        assert path.exists() and removed == []
    assert storage.sweep_expired(now=111) == [identity]
    assert removed == [identity]


def test_expiry_between_nested_operations_is_not_renewed(source):
    storage, identity, path, _ = source
    with storage.lease(identity):
        assert storage.sweep_expired(now=109) == []
        with storage.lease(identity):
            assert storage.sweep_expired(now=110) == []
        assert storage.sweep_expired(now=110) == []
        assert path.stat().st_mtime == 100
    assert storage.sweep_expired(now=110) == [identity]


@pytest.mark.parametrize("nested", [False, True])
def test_exception_releases_only_its_lease(source, nested):
    storage, identity, path, _ = source
    with storage.lease(identity):
        if nested:
            with pytest.raises(RuntimeError):
                with storage.lease(identity):
                    raise RuntimeError("synthetic callback error")
            assert storage.delete(identity) is False
        else:
            assert path.exists()
    with pytest.raises(RuntimeError):
        with storage.lease(identity):
            raise RuntimeError("synthetic outer error")
    assert storage.delete(identity) is True


def test_overlapping_threads_release_in_acquisition_order(source):
    storage, identity, path, _ = source
    entered = [Event(), Event()]
    release = [Event(), Event()]

    def worker(index):
        with storage.lease(identity):
            entered[index].set()
            assert release[index].wait(5)

    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(worker, 0)
        assert entered[0].wait(5)
        second = pool.submit(worker, 1)
        try:
            assert entered[1].wait(5)
            assert storage.sweep_expired(now=111) == []
            release[0].set()
            first.result(timeout=5)
            assert storage.delete(identity) is False
            assert storage.sweep_expired(now=111) == []
            assert path.exists()
        finally:
            for event in release:
                event.set()
            first.result(timeout=5)
            second.result(timeout=5)
    assert storage.sweep_expired(now=111) == [identity]


def test_lease_is_not_a_write_lock_or_a_source_authenticity_claim(source):
    storage, identity, path, _ = source
    with storage.lease(identity):
        with ThreadPoolExecutor(max_workers=1) as pool:
            pool.submit(path.write_bytes, b"changed synthetic bytes").result(timeout=5)
        assert path.read_bytes() != b"synthetic source"
        assert storage.delete(identity) is False
    assert storage.delete(identity) is True


def test_external_unlink_is_not_prevented_or_revived(source):
    storage, identity, path, _ = source
    with storage.lease(identity):
        with ThreadPoolExecutor(max_workers=1) as pool:
            pool.submit(path.unlink).result(timeout=5)
        assert not path.exists()
    assert identity not in storage._active_ids
