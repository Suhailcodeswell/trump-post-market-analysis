"""Export Power BI PDF pages as PNGs for the portfolio website."""

from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "powerbi" / "Trump report 1.pdf"
OUT = ROOT / "website" / "public" / "assets" / "charts"


def main() -> None:
    if not PDF.exists():
        raise FileNotFoundError(f"Missing PDF: {PDF}")
    OUT.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    n = len(doc)
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        out_path = OUT / f"slide-{i:02d}.png"
        pix.save(out_path)
        print(f"Wrote {out_path.name}")
    doc.close()
    print(f"Exported {n} slides to {OUT}")


if __name__ == "__main__":
    main()
