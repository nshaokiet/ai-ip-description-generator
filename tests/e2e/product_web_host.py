"""Trusted S1 test host. Offline certificates; the real protected approval path.

This harness is not imported by application runtime and never approves via HTTP.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import json
import os

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.app.local_product_web import run
from backend.app.services.product_web_host_control import (
    SecurityError, create_private_dir, restrict_owned,
)
from tests.e2e.provider_tripwire import ProviderTripwire, sanitize_provider_environment


def prepare(root: Path, hostname="localhost"):
    root = restrict_owned(root)
    state = create_private_dir(root / "state")
    tls = create_private_dir(root / "tls")
    executable = shutil.which("openssl") or next((str(path) for path in (
        Path("C:/Program Files/Git/mingw64/bin/openssl.exe"),
        Path("C:/Program Files/Git/usr/bin/openssl.exe"),
    ) if path.is_file()), None)
    if not executable:
        raise SecurityError()
    certificate, key = tls / "certificate.pem", tls / "private.pem"
    subprocess.run([
        executable, "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-sha256",
        "-days", "1", "-subj", "/CN=" + hostname,
        "-addext", "subjectAltName=DNS:" + hostname,
        "-keyout", str(key), "-out", str(certificate),
    ], check=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
       stderr=subprocess.DEVNULL, timeout=15)
    restrict_owned(key)
    restrict_owned(certificate)
    return state, certificate, key


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--reuse", action="store_true")
    parser.add_argument("--synthetic", action="store_true")
    args = parser.parse_args()
    sanitize_provider_environment()
    os.environ["AI_IP_ENABLE_LOCAL_ORCHESTRATION_API"] = "0"
    os.environ["AI_IP_ENABLE_LOCAL_SYNTHETIC_V2_API"] = "0"
    guard = ProviderTripwire().install()
    try:
        material = ((args.root / "state", args.root / "tls/certificate.pem", args.root / "tls/private.pem")
                    if args.reuse else prepare(args.root))
        run(*material, synthetic_enabled=args.synthetic)
    except (Exception, KeyboardInterrupt):
        print("S1 test host unavailable.", file=sys.stderr)
        raise SystemExit(1)
    finally:
        try:
            guard.assert_no_unexpected_activity()
            (args.root / "provider.json").write_text(json.dumps(guard.snapshot()), encoding="utf-8")
        finally:
            guard.close()
