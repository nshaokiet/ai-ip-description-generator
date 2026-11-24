"""Real C1 boundary with existing admitted fixtures and deterministic callbacks."""
import os
from concurrent.futures import ThreadPoolExecutor

import pytest

from tests.backend.test_product_synthetic_workflow import host, register
from backend.app.services.preapi_source_custody import CustodyError
from tests.e2e.provider_tripwire import ProviderTripwire


@pytest.mark.parametrize("name", ["controller.pdf", "research-b.docx"])
@pytest.mark.parametrize("mutation", ["rewrite", "unlink", "ttl_sweep"])
def test_c1_rechecks_source_after_runtime_and_keeps_outer_lease(host, name, mutation):
    document_id, payload = register(host, name)
    storage = host.app.state.document_storage
    path = storage.path_for(document_id)

    def concurrent_action():
        if mutation == "rewrite":
            path.write_bytes(b"x" * len(payload))
        elif mutation == "unlink":
            path.unlink()
        else:
            os.utime(path, (100, 100))
            assert storage.sweep_expired(now=100 + storage.ttl_seconds) == []

    def callback(analysis):
        with ThreadPoolExecutor(max_workers=1) as pool:
            pool.submit(concurrent_action).result(timeout=5)

    host.runtime.mutate = callback
    with ProviderTripwire() as tripwire:
        if mutation == "ttl_sweep":
            ref = host.workflow.start(document_id)
            assert host.workflow.review(ref).originals
        else:
            with pytest.raises(CustodyError) as error:
                host.workflow.start(document_id)
            assert error.value.code == ("SOURCE_HASH_MISMATCH" if mutation == "rewrite" else "INTAKE_REJECTED")
            assert not host.workflow._handles
        tripwire.assert_no_unexpected_activity()
        assert all(value == 0 for value in tripwire.snapshot().values())
    assert not path.exists()
    assert host.app.state.document_registry.get(document_id) is None
