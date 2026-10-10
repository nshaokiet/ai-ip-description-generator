"""Explicit, internal-only synthetic P2-006 four-file QA generation helper.

Run from repository root: python tests/backend/render_p2_006_synthetic_qa.py DEST_DIR
DEST_DIR must exist. Never use confidential or real research sources.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from test_uspto_document_package_v1 import inputs, run
from backend.app.services.uspto_offline_renderer import render_uspto_document_package


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: render_p2_006_synthetic_qa.py EXISTING_OUTPUT_DIR")
    originals = inputs()
    package = run(originals)
    output = render_uspto_document_package(package, **originals, output_dir=Path(sys.argv[1]))
    for name, path in output.items():
        print(name, path, path.stat().st_size)


if __name__ == "__main__":
    main()
