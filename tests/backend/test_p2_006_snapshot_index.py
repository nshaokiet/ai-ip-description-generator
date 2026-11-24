"""Synthetic transient/permanent APT tests: no network, sudo or package install."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "p2_006_snapshot_index", Path(__file__).with_name("p2_006_snapshot_index.py")
)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)

SNAPSHOT = "20261009T000000Z"


def apt_dir(tmp_path: Path) -> Path:
    p = tmp_path / "apt"
    p.mkdir()
    (p / "sources.list").write_text(
        "deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] "
        f"https://snapshot.ubuntu.com/ubuntu/{SNAPSHOT} noble main universe\n"
    )
    return p


def index_files(cmd: list[str]) -> Path:
    index = cmd.index("Dir::Etc::sourceparts=-")
    assert index > 0
    state = next(s.split("=", 1)[1] for s in cmd if s.startswith("Dir::State::lists="))
    return Path(state)


def fake_runner(statuses, snapshot=SNAPSHOT):
    calls = []
    queue = list(statuses)

    def run(cmd, **kwargs):
        calls.append(cmd)
        assert cmd[:2] == ["sudo", "apt-get"]
        assert cmd[-2:] == ["update", "-qq"]
        assert "APT::Update::Error-Mode=any" in cmd
        assert "Acquire::Retries=0" in cmd
        assert "Dir::Etc::sourceparts=-" in cmd
        status, code, complete = queue.pop(0)
        if complete:
            lists = index_files(cmd)
            for suite in module.SUITES:
                module._inrelease_path(lists, snapshot, suite).write_text("signed-index")
                for component in module.COMPONENTS:
                    (lists / f"snapshot.ubuntu.com_ubuntu_{snapshot}_dists_{suite}_{component}_binary-amd64_Packages.lz4").write_bytes(b"verified-package-index")
        return subprocess.CompletedProcess(cmd, code, "", status)

    return run, calls


def transient(status, suite="noble"):
    return (f"W: Failed to fetch https://snapshot.ubuntu.com/ubuntu/{SNAPSHOT}/"
            f"dists/{suite}/InRelease  {status}  Service Unavailable\n"
            "W: Some index files failed to download.\n")


def test_success_first_attempt(tmp_path):
    run, calls = fake_runner([("", 0, True)])
    path = module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run)
    assert path.name == "lists-1"
    assert len(calls) == 1


@pytest.mark.parametrize("code", [502, 503])
def test_transient_failure_then_success_with_fresh_lists(tmp_path, code):
    run, calls = fake_runner([(transient(code), 100, False), ("", 0, True)])
    delays = []
    result = module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run, sleeper=delays.append)
    assert result.name == "lists-2"
    assert index_files(calls[0]) != index_files(calls[1])
    assert delays == [2]


def test_two_transients_then_success(tmp_path):
    run, calls = fake_runner([(transient(502), 100, False),
                              (transient(503), 100, False), ("", 0, True)])
    delays = []
    assert module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run,
                                          sleeper=delays.append).name == "lists-3"
    assert delays == [2, 5]
    assert len(set(index_files(c) for c in calls)) == 3


def test_persistent_transient_fails_after_three(tmp_path):
    run, calls = fake_runner([(transient(503), 100, False)] * 3)
    delays = []
    with pytest.raises(module.SnapshotIndexError, match="exhausted 3 attempts"):
        module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run, sleeper=delays.append)
    assert len(calls) == 3 and delays == [2, 5]


def test_strict_apt_e_summary_with_only_pinned_http503_is_retryable(tmp_path):
    diagnostic = transient(503).replace("W: Failed to fetch", "E: Failed to fetch")
    diagnostic = diagnostic.replace("W: Some index files failed to download.", module.INDEX_SUMMARY)
    run, calls = fake_runner([(diagnostic, 100, False), ("", 0, True)])
    delays = []
    assert module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run,
                                          sleeper=delays.append).name == "lists-2"
    assert len(calls) == 2 and delays == [2]


def test_apt_exit_zero_but_partial_index_warning_must_retry(tmp_path):
    run, calls = fake_runner([(transient(502), 0, False), ("", 0, True)])
    assert module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run,
                                          sleeper=lambda _: None).name == "lists-2"
    assert len(calls) == 2


def test_apt_success_without_complete_indexes_fails_closed(tmp_path):
    run, calls = fake_runner([("", 0, False)])
    with pytest.raises(module.SnapshotIndexError, match="complete=False"):
        module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run)
    assert len(calls) == 1


@pytest.mark.parametrize("bad", [
    transient(404),
    "E: The repository is not signed.\n" + transient(503),
    "W: GPG error: NO_PUBKEY 123456\n" + transient(502),
    "E: Hash Sum mismatch\n" + transient(503),
    transient(503) + "W: Failed to fetch https://evil.example.org/Release  502 Bad Gateway\n",
    transient(503) + "E: Sub-process returned an error code\n",
])
def test_permanent_security_or_mixed_error_never_retried(tmp_path, bad):
    run, calls = fake_runner([(bad, 100, False)])
    with pytest.raises(module.SnapshotIndexError, match="retryable=false"):
        module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run)
    assert len(calls) == 1


@pytest.mark.parametrize("bad", ["latest", "2026-10-09", "../20261009T000000Z", ""])
def test_invalid_snapshot_id_rejected_before_apt(tmp_path, bad):
    run, calls = fake_runner([])
    with pytest.raises(module.SnapshotIndexError, match="Invalid pinned"):
        module.update_snapshot_indexes(apt_dir(tmp_path), bad, runner=run)
    assert not calls


def test_missing_sources_fails_before_apt(tmp_path):
    run, calls = fake_runner([])
    with pytest.raises(module.SnapshotIndexError, match="sources.list"):
        module.update_snapshot_indexes(tmp_path, SNAPSHOT, runner=run)
    assert not calls


def test_installer_keeps_exact_pins_and_does_not_install_on_retry_failure():
    text = Path(__file__).with_name("install_p2_006_qa.sh").read_text()
    assert 'test "$VERSION_ID" = "24.04"' in text
    assert 'test "$(dpkg --print-architecture)" = "amd64"' in text
    assert "signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg" in text
    assert 'verified_lists="$(python ' in text
    assert text.index('verified_lists="$(python ') < text.index('sudo apt-get "${options[@]}" install')
    assert '--no-install-recommends --allow-downgrades "${packages[@]}"' in text
    assert "verify_p2_006_qa_environment.py" in text
    assert "snapshot.ubuntu.com" in text
    assert "continue-on-error" not in text


@pytest.mark.parametrize("summary", [
    module.INDEX_SUMMARY,
    module.INDEX_SUMMARY.replace("E:", "W:", 1),
])
def test_partial_index_summary_alone_cannot_pass_with_exit_zero_and_inrelease_files(tmp_path, summary):
    run, calls = fake_runner([(summary, 0, True)])
    delays = []
    with pytest.raises(module.SnapshotIndexError, match="retryable=false"):
        module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run,
                                       sleeper=delays.append)
    assert len(calls) == 1 and delays == []


@pytest.mark.parametrize("bad", [
    f"E: Failed to fetch https://snapshot.ubuntu.com/ubuntu/{SNAPSHOT}/pool/main/example.deb  502 Bad Gateway",
    f"E: Failed to fetch https://snapshot.ubuntu.com/ubuntu/{SNAPSHOT}/pool/main/example.deb  503 Service Unavailable",
])
def test_package_acquisition_is_not_an_index_retry(tmp_path, bad):
    run, calls = fake_runner([(bad, 100, True)])
    delays = []
    with pytest.raises(module.SnapshotIndexError, match="retryable=false"):
        module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run,
                                       sleeper=delays.append)
    assert len(calls) == 1 and delays == []


@pytest.mark.parametrize("code", [500, 502, 503])
@pytest.mark.parametrize("path", [
    "noble/InRelease", "noble-updates/main/binary-amd64/Packages.gz",
    "noble-security/universe/binary-all/Packages.xz",
    "noble/main/i18n/Translation-en.gz", "noble/universe/cnf/Commands-amd64",
])
def test_allowed_transient_index_paths_retry(tmp_path, code, path):
    diagnostic = f"E: Failed to fetch https://snapshot.ubuntu.com/ubuntu/{SNAPSHOT}/dists/{path}  {code} Server Error\n" + module.INDEX_SUMMARY
    run, calls = fake_runner([(diagnostic, 100, False), ("", 0, True)])
    delays = []
    assert module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run,
                                          sleeper=delays.append).name == "lists-2"
    assert len(calls) == 2 and delays == [2]


def test_mixed_transient_component_indexes_retry(tmp_path):
    diagnostic = "\n".join(
        f"E: Failed to fetch https://snapshot.ubuntu.com/ubuntu/{SNAPSHOT}/dists/{p}  {code} Server Error"
        for p, code in [("noble/InRelease", 502), ("noble/main/binary-amd64/Packages.gz", 500),
                        ("noble-updates/universe/i18n/Translation-en", 503)])
    run, calls = fake_runner([(diagnostic, 100, False), ("", 0, True)])
    assert module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run,
                                          sleeper=lambda _: None).name == "lists-2"


@pytest.mark.parametrize("url", [
    f"https://snapshot.ubuntu.com/ubuntu/{SNAPSHOT}/dists/noble/main/binary-arm64/Packages.gz",
    f"https://snapshot.ubuntu.com/ubuntu/{SNAPSHOT}/dists/noble/restricted/binary-amd64/Packages",
    f"https://snapshot.ubuntu.com/ubuntu/{SNAPSHOT}/dists/noble/main/i18n/Translation-fr",
    f"https://snapshot.ubuntu.com/ubuntu/{SNAPSHOT}/dists/noble/main/binary-amd64/Packages?bypass=1",
    f"https://snapshot.ubuntu.com/ubuntu/{SNAPSHOT}/dists/noble/main/../InRelease",
    f"https://snapshot.ubuntu.com.evil.example/ubuntu/{SNAPSHOT}/dists/noble/InRelease",
    "https://snapshot.ubuntu.com/ubuntu/20261010T000000Z/dists/noble/InRelease",
])
def test_unexpected_index_target_never_retried(tmp_path, url):
    run, calls = fake_runner([(transient(503) + f"E: Failed to fetch {url}  500 Server Error\n", 100, False)])
    with pytest.raises(module.SnapshotIndexError, match="retryable=false"):
        module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run)
    assert len(calls) == 1


@pytest.mark.parametrize("failure", [transient(403), transient(404), "E: BADSIG archive\n", "E: Hash Sum mismatch\n"])
def test_mixed_transient_permanent_never_retried(tmp_path, failure):
    run, calls = fake_runner([(transient(503) + failure, 100, False)])
    with pytest.raises(module.SnapshotIndexError, match="retryable=false"):
        module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run)
    assert len(calls) == 1


def test_existing_attempt_directory_cannot_be_reused(tmp_path):
    folder = apt_dir(tmp_path)
    (folder / "lists-1").mkdir()
    run, calls = fake_runner([])
    with pytest.raises(FileExistsError):
        module.update_snapshot_indexes(folder, SNAPSHOT, runner=run)
    assert not calls


@pytest.mark.parametrize("missing", ["InRelease", "Packages", "empty", "partial", "wrong-pin"])
def test_missing_required_index_cannot_be_accepted(tmp_path, missing):
    original, calls = fake_runner([("", 0, True)])
    def runner(cmd, **kwargs):
        result = original(cmd, **kwargs)
        lists = index_files(cmd)
        path = (module._inrelease_path(lists, SNAPSHOT, "noble") if missing == "InRelease" else
                lists / f"snapshot.ubuntu.com_ubuntu_{SNAPSHOT}_dists_noble_main_binary-amd64_Packages.lz4")
        if missing == "empty":
            path.write_bytes(b"")
        elif missing == "partial":
            path.rename(lists / "partial" / path.name)
        elif missing == "wrong-pin":
            path.rename(lists / path.name.replace(SNAPSHOT, "20261010T000000Z"))
        else:
            path.unlink()
        return result
    with pytest.raises(module.SnapshotIndexError, match="complete=False"):
        module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=runner)
    assert len(calls) == 1


def test_failed_attempt_complete_files_never_satisfy_next_attempt(tmp_path):
    run, calls = fake_runner([(transient(500), 100, True), ("", 0, False)])
    with pytest.raises(module.SnapshotIndexError, match="complete=False"):
        module.update_snapshot_indexes(apt_dir(tmp_path), SNAPSHOT, runner=run, sleeper=lambda _: None)
    assert len(calls) == 2 and index_files(calls[0]) != index_files(calls[1])
