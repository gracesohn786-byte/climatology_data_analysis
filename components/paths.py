"""Resolve paths to research data and figures relative to repository root."""
from __future__ import annotations

from pathlib import Path

# streamlit_app/components/paths.py → streamlit_app is two levels up
APP_DIR = Path(__file__).resolve().parent.parent


def _find_repo_root(start: Path) -> Path:
    """Directory containing Caucasus_Weather_Stations.

    Handles:
    - Local: repo root with streamlit_app/ subfolder
    - Streamlit Cloud: app may live at repo root (no streamlit_app) or in streamlit_app/
    """
    cur = start.resolve()
    for _ in range(10):
        if (cur / "Caucasus_Weather_Stations").is_dir():
            return cur
        # e.g. cwd is streamlit_app/ but data dirs are siblings at repo root
        parent = cur.parent
        if (parent / "Caucasus_Weather_Stations").is_dir():
            return parent
        if cur.parent == cur:
            break
        cur = parent
    return start.parent


REPO_ROOT = _find_repo_root(APP_DIR)

CAUCASUS = REPO_ROOT / "Caucasus_Weather_Stations"
SENAMHI = REPO_ROOT / "Senamhi_Weather_Stations"
LASCAR = REPO_ROOT / "Peru_Lascar_EDW_temperature_humidity"
POSTER_PDF = REPO_ROOT / "poster" / "Stars 2026 poster.pdf"


def p(*parts: str) -> Path:
    """Path under repo root."""
    return REPO_ROOT.joinpath(*parts)


def exists(path: Path) -> bool:
    return path.is_file() or path.is_dir()
