"""A wrong package/build must block the QA conversion, even if tools exist."""
import json
import subprocess

import pytest

from verify_p2_006_qa_environment import DEFINITION, verify


@pytest.mark.parametrize("mismatch", [None, "package", "office", "poppler"])
def test_exact_qa_environment_fails_closed(monkeypatch, mismatch):
    expected = json.loads(DEFINITION.read_text())

    def output(command, **kwargs):
        if command[0] == "dpkg-query":
            if mismatch == "package" and command[-1] == "libreoffice-writer":
                return "4:24.2.7-0ubuntu0.24.04.2"
            return expected["packages"][command[-1]]
        return "LibreOffice " + ("25.2.0.1" if mismatch == "office" else expected["libreoffice_runtime"]) + " 420(Build:7)"

    def run(command, **kwargs):
        version = "25.01.0" if mismatch == "poppler" else expected["poppler_runtime"]
        return subprocess.CompletedProcess(command, 0, "", "pdftoppm version "+version)

    monkeypatch.setattr(subprocess, "check_output", output)
    monkeypatch.setattr(subprocess, "run", run)
    if mismatch:
        with pytest.raises(RuntimeError, match="mismatch"):
            verify()
    else:
        assert verify()["installed_packages"] == expected["packages"]
