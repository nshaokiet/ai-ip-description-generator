"""Print text from an actual browser-downloaded DOCX using only the stdlib."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile


def main() -> None:
    path = Path(sys.argv[1])
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    paragraphs: list[str] = []
    with ZipFile(path) as archive:
        members = [
            name for name in archive.namelist()
            if name == "word/document.xml"
            or name.startswith("word/header") and name.endswith(".xml")
            or name.startswith("word/footer") and name.endswith(".xml")
        ]
        if "word/document.xml" not in members:
            raise ValueError("DOCX has no document body")
        for name in members:
            root = ElementTree.fromstring(archive.read(name))
            for paragraph in root.iter(f"{namespace}p"):
                value = "".join(node.text or "" for node in paragraph.iter(f"{namespace}t"))
                if value:
                    paragraphs.append(value)
    print(json.dumps({"text": "\n".join(paragraphs)}))


if __name__ == "__main__":
    main()
