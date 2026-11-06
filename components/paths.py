"""Resolve paths to research data and figures relative to repository root."""
from __future__ import annotations

from pathlib import Path

# streamlit_app/components/paths.py → APP_DIR = streamlit_app/
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

# Bundled copy for app-only GitHub deployments (run scripts/bundle_data.py)
BUNDLE_DIR = APP_DIR / "data"


def _region_or_bundle(name: str) -> Path:
    bundled = BUNDLE_DIR / name
    if bundled.is_dir():
        return bundled
    return REPO_ROOT / name


CAUCASUS = _region_or_bundle("Caucasus_Weather_Stations")
SENAMHI = _region_or_bundle("Senamhi_Weather_Stations")
LASCAR = _region_or_bundle("Peru_Lascar_EDW_temperature_humidity")

# Poster: shipped under streamlit_app/poster/ or repo root poster/
_poster_candidates = [
    APP_DIR / "poster" / "Stars 2026 poster.pdf",
    REPO_ROOT / "poster" / "Stars 2026 poster.pdf",
]
POSTER_PDF = next((p for p in _poster_candidates if p.is_file()), _poster_candidates[0])


def p(*parts: str) -> Path:
    """Path under repo root."""
    return REPO_ROOT.joinpath(*parts)


def exists(path: Path) -> bool:
    return path.is_file() or path.is_dir()
