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


def senamhi_annual_lapse_rate_csv(historical: bool) -> Path:
    """Annual LR time series: canonical `derived/` names, then v3/v2 alternates.

    Canonical (network OLS, matches Peru Analysis copy text):
    - `derived/senamhi_annual_lapse_rate_1967_1992.csv`
    - `derived/senamhi_annual_lapse_rate_2004_2019.csv`

    If only fixed-station or older exports exist, fall back to `annual_lr_v3/` then `annual_LR_v2/`.
    """
    if historical:
        return resolve_under(
            SENAMHI,
            "derived/senamhi_annual_lapse_rate_1967_1992.csv",
            "annual_lr_v3/senamhi_annual_lapse_rate_fixed_trio_1967_1992.csv",
            "annual_lr_v3/senamhi_annual_lapse_rate_fixed_pair_relaxed_m7_1967_1992.csv",
            "annual_lr_v3/senamhi_annual_lapse_rate_fixed_pair_hist_relaxed_m6_1967_1992.csv",
            "annual_lr_v3/senamhi_annual_lapse_rate_fixed_pair_1967_1992.csv",
            "annual_LR_v2/senamhi_annual_lapse_rate_fixed_pair_1967_1992.csv",
        )
    return resolve_under(
        SENAMHI,
        "derived/senamhi_annual_lapse_rate_2004_2019.csv",
        "annual_lr_v3/senamhi_annual_lapse_rate_fixed_trio_2004_2019.csv",
        "annual_lr_v3/senamhi_annual_lapse_rate_fixed_pair_relaxed_m7_2004_2019.csv",
        "annual_lr_v3/senamhi_annual_lapse_rate_fixed_pair_2004_2019.csv",
        "annual_LR_v2/senamhi_annual_lapse_rate_fixed_pair_2004_2019.csv",
    )


def resolve_under(base: Path, *relative_paths: str) -> Path:
    """Return the first existing file under `base`; else the primary path (for error messages).

    Supports alternate folder layouts (e.g. `derived/plots/lapse_rate/` vs top-level analysis folders).
    """
    if not relative_paths:
        raise ValueError("resolve_under requires at least one relative path")
    for rel in relative_paths:
        p = base / rel.replace("\\", "/")
        if p.is_file():
            return p
    return base / relative_paths[0].replace("\\", "/")


# --- Reference PNGs (original figures) — try canonical paths then repo-specific alternates ---

def caucasus_png_annual_lr() -> Path:
    return resolve_under(
        CAUCASUS,
        "annual_LR_analysis/caucasus_annual_lapse_rate_timeseries_1959_1992.png",
        "annual_LR_analysis/caucasus_annual_lapse_rate_timeseries_1959_1992_(2).png",
        "derived/plots/lapse_rate/caucasus_annual_lapse_rate_timeseries_1959_1992.png",
    )


def caucasus_png_seasonal_lr_main() -> Path:
    return resolve_under(
        CAUCASUS,
        "seasonal_LR_analysis/caucasus_seasonal_lapse_rate_timeseries_1959_1992.png",
        "derived/plots/lapse_rate/caucasus_seasonal_lapse_rate_timeseries_1959_1992.png",
    )


def caucasus_png_seasonal_lr_old() -> Path:
    return resolve_under(
        CAUCASUS,
        "seasonal_LR_analysis/caucasus_seasonal_lapse_rate_timeseries_1959_1992_old.png",
    )


def caucasus_png_freezing_level() -> Path:
    return resolve_under(
        CAUCASUS,
        "FL_timeseries_analysis/caucasus_freezing_level_timeseries_1959_1992.png",
        "derived/plots/lapse_rate/caucasus_freezing_level_timeseries_1959_1992.png",
        "derived/plots/lapse_rate/caucasus_freezing_level_timeseries_1959_1992_ylim4000_11000.png",
        "derived/plots/lapse_rate/caucasus_freezing_level_timeseries_1959_1992_ylim2000_11000.png",
    )


def caucasus_png_climatology_scatter() -> Path:
    return resolve_under(
        CAUCASUS,
        "LR_Elevation_vs_Temp_Analysis/plot/caucasus_lapse_rate_climatology_elevation_vs_temp_1959_1992.png",
        "LR_Elevation_vs_Temp_Analysis/caucasus_lapse_rate_climatology_elevation_vs_temp_1959_1992.png",
    )


def senamhi_png_annual_lr(historical: bool) -> Path:
    if historical:
        return resolve_under(
            SENAMHI,
            "annual_LR_analysis/senamhi_annual_lapse_rate_1967_1992.png",
            "annual_lr_v3/senamhi_annual_lapse_rate_fixed_trio_1967_1992.png",
            "annual_lr_v3/senamhi_annual_lapse_rate_fixed_pair_relaxed_m7_1967_1992.png",
            "annual_LR_v2/senamhi_annual_lapse_rate_fixed_pair_1967_1992.png",
        )
    return resolve_under(
        SENAMHI,
        "annual_LR_analysis/senamhi_annual_lapse_rate_2004_2019.png",
        "annual_lr_v3/senamhi_annual_lapse_rate_fixed_trio_2004_2019.png",
        "annual_lr_v3/senamhi_annual_lapse_rate_fixed_pair_relaxed_m7_2004_2019.png",
        "annual_LR_v2/senamhi_annual_lapse_rate_fixed_pair_2004_2019.png",
    )


def senamhi_png_seasonal_lr_relaxed(historical: bool) -> Path:
    if historical:
        return resolve_under(
            SENAMHI,
            "seasonal_LR_analysis/senamhi_seasonal_lapse_rate_timeseries_1967_1992_relaxed_sf50_m3of4.png",
            "seasonal_LR_analysis/senamhi_seasonal_lapse_rate_timeseries_1967_1992_relaxed_sf67_m3of4.png",
            "seasonal_LR_analysis/senamhi_seasonal_lapse_rate_timeseries_1967_1992.png",
            "seasonal_lr_v2/senamhi_seasonal_lapse_rate_timeseries_1967_1992_fixed_pair_bv_aija_hist_relaxed_m2of4.png",
        )
    return resolve_under(
        SENAMHI,
        "seasonal_LR_analysis/senamhi_seasonal_lapse_rate_timeseries_2004_2019_relaxed_sf67_m3of4.png",
        "seasonal_LR_analysis/senamhi_seasonal_lapse_rate_timeseries_2004_2019.png",
        "seasonal_lr_v2/senamhi_seasonal_lapse_rate_timeseries_2004_2019_fixed_pair_bv_recuay_m3of4.png",
    )


def senamhi_png_freezing_level_sf33() -> Path:
    return resolve_under(
        SENAMHI,
        "FL_timeseries_analysis/senamhi_freezing_level_timeseries_1967_1992_sf33.png",
    )


def senamhi_png_freezing_level_sf50() -> Path:
    return resolve_under(
        SENAMHI,
        "FL_timeseries_analysis/senamhi_freezing_level_timeseries_1967_1992_sf50.png",
    )


def senamhi_png_freezing_level_sf67() -> Path:
    return resolve_under(
        SENAMHI,
        "FL_timeseries_analysis/senamhi_freezing_level_timeseries_2004_2019_sf67.png",
    )


def senamhi_png_freezing_level_fixedpair_cajatambo_chavin() -> Path:
    return resolve_under(
        SENAMHI,
        "FL_timeseries_v2/senamhi_freezing_level_timeseries_v2_fixedpair_cajatambo_chavin_1994_2019.png",
    )


def senamhi_png_fl_comparison_caucasus() -> Path:
    return resolve_under(
        SENAMHI,
        "FL_timeseries_analysis/freezing_level_trend_comparison_caucasus_vs_senamhi.png",
    )


def lascar_png_seasonal_timeseries(relaxed: bool) -> Path:
    if relaxed:
        return resolve_under(LASCAR, "seasonal_lr_analysis/lascar_seasonal_lr_timeseries_relaxed_2006_2025.png")
    return resolve_under(LASCAR, "seasonal_lr_analysis/lascar_seasonal_lr_timeseries_2006_2025.png")
