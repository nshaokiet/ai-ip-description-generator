"""Optional local QA image capture (requires pypdfium2==4.30.0)."""
from pathlib import Path
import sys
import pypdfium2


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("Usage: inspect_p2_006_pages.py PDF OUT_DIR [PAGE_INDEX...]")
    source, out = Path(sys.argv[1]), Path(sys.argv[2])
    if not source.is_file() or not out.is_dir():
        raise ValueError("PDF and pre-existing output directory required")
    doc = pypdfium2.PdfDocument(str(source))
    page_numbers = [int(n) for n in sys.argv[3:]] if len(sys.argv) > 3 else range(len(doc))
    for number in page_numbers:
        result = out / f"{source.stem}-p{number + 1:02}.png"
        doc[number].render(scale=2.5).to_pil().save(result)
        print(result)


if __name__ == "__main__":
    main()
