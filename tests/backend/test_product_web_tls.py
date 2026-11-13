"""Real offline certificate/key verification through the production launcher."""
import os
from pathlib import Path
import subprocess
import sys

import pytest

from tests.e2e.product_web_host import prepare, ROOT
from backend.app.services.product_web_host_control import restrict_owned


def check(certificate, key):
    environment = {**os.environ, "AIIP_S1_CERT": str(certificate), "AIIP_S1_KEY": str(key),
                   "AIIP_S1_PYTHON": sys.executable}
    return subprocess.run(["node", "frontend/tools/product-web-local-https.mjs", "--check-tls"],
                          cwd=ROOT, env=environment, capture_output=True, text=True, timeout=20)


def test_valid_tls_has_matching_key_localhost_san_and_private_owner(tmp_path):
    _, certificate, key = prepare(tmp_path)
    result = check(certificate, key)
    assert result.returncode == 0
    assert result.stdout == "TLS prerequisites verified.\n"
    assert not result.stderr
    assert "PRIVATE KEY" not in result.stdout


@pytest.mark.parametrize("fault", ["missing", "san", "mismatch", "corrupt", "permissions"])
def test_tls_fails_closed_on_actual_prerequisite_failure(tmp_path, fault):
    _, certificate, key = prepare(tmp_path, hostname="foreign.invalid" if fault == "san" else "localhost")
    if fault == "missing":
        key.unlink()
    elif fault == "mismatch":
        other = tmp_path / "other"
        other.mkdir()
        _, _, key = prepare(other)
    elif fault == "corrupt":
        certificate.write_text("invalid certificate", encoding="utf-8")
        restrict_owned(certificate)
    elif fault == "permissions":
        if os.name == "nt":
            from backend.app.services.product_web_host_control import _windows, C
            win, descriptor = _windows(), C.c_void_p()
            assert win.a.ConvertStringSecurityDescriptorToSecurityDescriptorW(
                f"D:P(A;;GA;;;{win.sid})(A;;GR;;;WD)", 1, C.byref(descriptor), None)
            try:
                assert win.a.SetFileSecurityW(str(key), 0x80000004, descriptor)
            finally:
                win.k.LocalFree(descriptor)
        else:
            key.chmod(0o644)
    result = check(certificate, key)
    assert result.returncode != 0
    assert result.stderr == "S1 local transport unavailable.\n"
    assert "PRIVATE KEY" not in result.stdout + result.stderr
