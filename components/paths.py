"""Resolve paths to research data and figures relative to repository root."""
from __future__ import annotations

from pathlib import Path

# streamlit_app/components/paths.py → APP_DIR = streamlit_app/
APP_DIR = Path(__file__).resolve().parent.parent


def _find_repo_root(start: Path) -> Path:
    """Directory that should contain `Caucasus_Weather_Stations/` (or `streamlit_app/data/` bundle).

    Handles:
    - Local: `streamlit_app/` under a repo root that has region folders next to it
    - Streamlit Cloud: app code may be **at** repo root (`components/` next to `pages/`), so `APP_DIR` is
      already the clone root — we must **not** fall back to `/mount/src`, which has no data.
    """
    start = start.resolve()
    cur: Path = start
    for _ in range(12):
        if (cur / "Caucasus_Weather_Stations").is_dir():
            return cur
        parent = cur.parent
        if parent != cur and (parent / "Caucasus_Weather_Stations").is_dir():
            return parent
        if parent == cur:
            break
        cur = parent
    # No Caucasus folder found walking up: sensible defaults
    if start.name == "streamlit_app" and (start / "components").is_dir():
        return start.parent
    # App-at-root layout: `start` is already the clone directory (e.g. …/climatology_data_analysis)
    return start


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


def _first_existing(*candidates: Path) -> Path:
    """Return the first path that exists; else the first candidate (for error messages)."""
    for p in candidates:
        if p.is_file():
            return p
    return candidates[0]


def caucasus_derived_csv(filename: str) -> Path:
    """Preferred: `Caucasus_Weather_Stations/derived/<file>`; fallback: same name directly under region folder."""
    base = CAUCASUS
    return _first_existing(base / "derived" / filename, base / filename)


def caucasus_completeness_summary_path() -> Path:
    """Audit subfolder, or flat `derived/<summary>.csv` if the user committed that layout."""
    name = "caucasus_station_completeness_summary_1959_1992.csv"
    return _first_existing(
        CAUCASUS / "derived" / "completeness_audit_1959_1992" / name,
        CAUCASUS / "derived" / name,
        CAUCASUS / name,
    )
