"""One-off: extract poster PDF text to assets/poster_extract.txt."""
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    raise SystemExit("Install pypdf: pip install pypdf")

APP_DIR = Path(__file__).resolve().parent.parent
POSTER = APP_DIR.parent / "poster" / "Stars 2026 poster.pdf"
OUT = APP_DIR / "assets" / "poster_extract.txt"

if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if not POSTER.is_file():
        raise SystemExit(f"Poster not found: {POSTER}")
    reader = PdfReader(str(POSTER))
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    OUT.write_text("\n\n".join(parts), encoding="utf-8")
    print("Wrote", OUT)
