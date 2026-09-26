"""CLI compatibility wrapper for Patent DOCX Template v1.0.0 rendering."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from backend.app.services.patent_docx_renderer import (  # noqa: E402
    OUTPUT_ROOT,
    TEMPLATE_PATH,
    prepare_context,
    validate_payload,
)
from backend.app.services.patent_docx_renderer import (  # noqa: E402
    render_patent_docx as render_patent_docx_payload,
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as source:
        value = json.load(source)
    if not isinstance(value, dict):
        raise ValueError("Input JSON root must be an object.")
    return value


def render_patent_docx(
    input_path: Path,
    output_path: Path,
    template_path: Path = TEMPLATE_PATH,
) -> Path:
    """Load a JSON fixture and delegate rendering to the production service."""

    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve()
    template_path = Path(template_path).resolve()
    if not input_path.is_file():
        raise FileNotFoundError("Input JSON is unavailable.")
    if template_path != TEMPLATE_PATH.resolve():
        raise ValueError("Only the canonical DOCX template is supported.")
    if output_path == input_path:
        raise ValueError("Output path must not overwrite the input JSON.")
    return render_patent_docx_payload(_load_json(input_path), output_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_docx", type=Path)
    args = parser.parse_args(argv)
    try:
        rendered = render_patent_docx(args.input_json, args.output_docx)
        print(f"Rendered DOCX: {rendered.relative_to(REPOSITORY_ROOT)}")
        return 0
    except Exception as error:  # safe CLI boundary; never print payload content
        print(
            f"DOCX rendering failed: {type(error).__name__}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
