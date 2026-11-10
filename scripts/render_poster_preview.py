"""
Render Stars 2026 poster PDF → PNG preview for Streamlit Home.

Requires PyMuPDF (one-time local tool; not needed on Streamlit Cloud if the PNG is committed):

  pip install pymupdf
  python streamlit_app/scripts/render_poster_preview.py
"""
from __future__ import annotations

from pathlib import Path


def main() -> None:
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz  # type: ignore
        except ImportError as e:
            raise SystemExit("Install PyMuPDF first: pip install pymupdf") from e

    app = Path(__file__).resolve().parent.parent
    candidates = [
        app / "poster" / "Stars 2026 poster.pdf",
        app.parent / "poster" / "Stars 2026 poster.pdf",
        app.parent / "poster" / "weather_station_analysis_poster.pdf",
    ]
    pdf = next((p for p in candidates if p.is_file()), None)
    if pdf is None:
        raise SystemExit("Poster PDF not found under streamlit_app/poster/ or repo poster/.")

    out = app / "poster" / "Stars_2026_poster_preview.png"
    out.parent.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
    pix.save(str(out))
    doc.close()
    print(f"Wrote {out} ({out.stat().st_size} bytes) from {pdf.name}")


if __name__ == "__main__":
    main()
