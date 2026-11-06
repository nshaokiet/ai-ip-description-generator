"""Fail-closed, bounded APT index acquisition for the pinned P2-006 QA snapshot.

This helper only chooses an isolated, freshly downloaded signed-index directory.
It never installs packages, changes the snapshot/pins, or accepts live apt indexes.
"""

from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable

SNAPSHOT_RE = re.compile(r"^\d{8}T\d{6}Z$")
SUITES = ("noble", "noble-updates", "noble-security")
RETRY_DELAYS = (2, 5)
BAD_SECURITY_MARKERS = (
    "NO_PUBKEY", "BADSIG", "EXPKEYSIG", "REVKEYSIG", "Hash Sum mismatch",
    "is not signed", "does not have a Release file", "Clearsigned file isn't valid",
    "signatures couldn't be verified", "Signature verification failed",
)


class SnapshotIndexError(RuntimeError):
    """APT index acquisition failed without any allowed fallback."""


def _inrelease_path(lists: Path, snapshot: str, suite: str) -> Path:
    return lists / f"snapshot.ubuntu.com_ubuntu_{snapshot}_dists_{suite}_InRelease"


def _transient_only(diagnostics: str, snapshot: str) -> bool:
    """Accept only explicitly reported HTTP 502/503 on the three pinned indexes."""
    if any(marker.lower() in diagnostics.lower() for marker in BAD_SECURITY_MARKERS):
        return False
    expected = re.compile(
        r"^(?:W|E): Failed to fetch https://snapshot\.ubuntu\.com/ubuntu/"
        + re.escape(snapshot)
        + r"/dists/(?:noble|noble-updates|noble-security)/InRelease\s+(?:502|503)\b"
    )
    failed_fetch = [line.strip() for line in diagnostics.splitlines()
                    if "Failed to fetch" in line]
    if not failed_fetch or not all(expected.search(line) for line in failed_fetch):
        return False
    # Do not retry a mixed permanent or unknown APT error, even when a 503 exists.
    for line in diagnostics.splitlines():
        if line.startswith("E:") and "Failed to fetch" not in line:
            return False
    return True


def update_snapshot_indexes(
    qa_apt: Path, snapshot: str, *,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    sleeper: Callable[[float], None] = time.sleep,
) -> Path:
    """Return only a complete fresh index set; never reuse a failed attempt's lists."""
    if not SNAPSHOT_RE.fullmatch(snapshot):
        raise SnapshotIndexError("Invalid pinned Ubuntu snapshot identifier")
    if not qa_apt.is_dir() or not (qa_apt / "sources.list").is_file():
        raise SnapshotIndexError("Isolated pinned sources.list is missing")

    for attempt in range(1, len(RETRY_DELAYS) + 2):
        lists = qa_apt / f"lists-{attempt}"
        lists.mkdir(mode=0o755)
        (lists / "partial").mkdir(mode=0o755)
        lists.chmod(0o755)
        (lists / "partial").chmod(0o755)
        args = [
            "sudo", "apt-get",
            "-o", f"Dir::Etc::sourcelist={qa_apt / 'sources.list'}",
            "-o", "Dir::Etc::sourceparts=-",
            "-o", f"Dir::State::lists={lists}",
            "-o", "Acquire::Check-Valid-Until=false",
            "-o", "APT::Update::Error-Mode=any",
            "-o", "Acquire::Retries=0",
            "-o", "Acquire::http::Timeout=30",
            "-o", "Acquire::https::Timeout=30",
            "update", "-qq",
        ]
        result = runner(args, text=True, capture_output=True, check=False)
        diagnostics = (result.stdout or "") + "\n" + (result.stderr or "")
        print(f"[P2-006 pinned index attempt {attempt}/{len(RETRY_DELAYS)+1}]", file=sys.stderr)
        if diagnostics.strip():
            print(diagnostics.rstrip(), file=sys.stderr)
        complete = all(_inrelease_path(lists, snapshot, suite).is_file()
                       and _inrelease_path(lists, snapshot, suite).stat().st_size > 0
                       for suite in SUITES)
        has_fetch_errors = "Failed to fetch" in diagnostics
        has_integrity_error = any(marker.lower() in diagnostics.lower()
                                  for marker in BAD_SECURITY_MARKERS)
        has_other_error = any(line.startswith("E:") and "Failed to fetch" not in line
                              for line in diagnostics.splitlines())
        if result.returncode == 0 and complete and not (has_fetch_errors or has_integrity_error or has_other_error):
            return lists
        retryable = _transient_only(diagnostics, snapshot)
        if not retryable:
            raise SnapshotIndexError(
                f"Pinned snapshot index acquisition failed closed at attempt {attempt}; "
                f"apt_exit={result.returncode}, complete={complete}, retryable=false"
            )
        if attempt > len(RETRY_DELAYS):
            raise SnapshotIndexError("Pinned snapshot index acquisition exhausted 3 attempts (HTTP 502/503)")
        delay = RETRY_DELAYS[attempt - 1]
        print(f"[P2-006 pinned index retry after {delay}s; fresh lists required]", file=sys.stderr)
        sleeper(delay)
    raise AssertionError("Unreachable index retry state")


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: p2_006_snapshot_index.py <isolated-apt-dir> <pinned-snapshot>", file=sys.stderr)
        return 2
    try:
        verified_lists = update_snapshot_indexes(Path(sys.argv[1]), sys.argv[2])
    except (SnapshotIndexError, OSError) as exc:
        print(f"P2-006 pinned index FAILURE: {exc}", file=sys.stderr)
        return 1
    print(verified_lists)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
