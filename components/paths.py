"""Resolve paths to research data and figures relative to repository root."""
from __future__ import annotations

from pathlib import Path

# streamlit_app/components/paths.py -> repo root is two levels up
APP_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = APP_DIR.parent

CAUCASUS = REPO_ROOT / "Caucasus_Weather_Stations"
SENAMHI = REPO_ROOT / "Senamhi_Weather_Stations"
LASCAR = REPO_ROOT / "Peru_Lascar_EDW_temperature_humidity"
POSTER_PDF = REPO_ROOT / "poster" / "Stars 2026 poster.pdf"


def p(*parts: str) -> Path:
    """Path under repo root."""
    return REPO_ROOT.joinpath(*parts)


def exists(path: Path) -> bool:
    return path.is_file() or path.is_dir()
