"""Fail closed on package/runtime mismatch before any P2-006 CI conversion."""
from pathlib import Path
import json
import re
import subprocess

DEFINITION = Path(__file__).with_name("p2_006_qa_environment.json")


def verify() -> dict:
    expected = json.loads(DEFINITION.read_text())
    actual = {}
    for package, revision in expected["packages"].items():
        value = subprocess.check_output(
            ["dpkg-query", "-W", "-f=${Version}", package], text=True
        ).strip()
        if value != revision:
            raise RuntimeError(f"QA package mismatch: {package}: {value} != {revision}")
        actual[package] = value
    office = subprocess.check_output(["soffice", "--version"], text=True).strip()
    poppler = subprocess.run(["pdftoppm", "-v"], capture_output=True, text=True, check=True)
    poppler_version = (poppler.stdout + poppler.stderr).strip()
    if not re.match(r"^LibreOffice " + re.escape(expected["libreoffice_runtime"]) + r"(?:\s|$)", office):
        raise RuntimeError("Pinned LibreOffice runtime mismatch")
    if not re.match(r"^pdftoppm version " + re.escape(expected["poppler_runtime"]) + r"(?:\s|$)", poppler_version):
        raise RuntimeError("Pinned Poppler runtime mismatch")
    return {"definition": expected, "installed_packages": actual,
            "libreoffice": office, "poppler": poppler_version}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
