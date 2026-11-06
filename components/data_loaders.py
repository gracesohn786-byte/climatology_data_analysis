"""Cached loaders for derived analysis CSVs."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from components.paths import CAUCASUS, LASCAR, SENAMHI

# Bump when path logic changes so Streamlit Cloud does not serve stale empty cached frames.
_DATA_CACHE_VERSION = "v3_bundle"


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.is_file():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_caucasus_annual_lr(_ver: str = _DATA_CACHE_VERSION) -> pd.DataFrame:
    return _read_csv(CAUCASUS / "derived" / "caucasus_annual_lapse_rate_timeseries_1959_1992.csv")


@st.cache_data(show_spinner=False)
def load_caucasus_seasonal_lr_long(_ver: str = _DATA_CACHE_VERSION) -> pd.DataFrame:
    return _read_csv(CAUCASUS / "derived" / "caucasus_seasonal_lapse_rate_long_1959_1992.csv")


@st.cache_data(show_spinner=False)
def load_caucasus_seasonal_diag(_ver: str = _DATA_CACHE_VERSION) -> pd.DataFrame:
    return _read_csv(CAUCASUS / "derived" / "caucasus_seasonal_lapse_rate_diagnostics_1959_1992.csv")


@st.cache_data(show_spinner=False)
def load_caucasus_fl(_ver: str = _DATA_CACHE_VERSION) -> pd.DataFrame:
    return _read_csv(CAUCASUS / "derived" / "caucasus_freezing_level_timeseries_1959_1992.csv")


@st.cache_data(show_spinner=False)
def load_caucasus_climatology(_ver: str = _DATA_CACHE_VERSION) -> pd.DataFrame:
    df = _read_csv(CAUCASUS / "derived" / "caucasus_station_annual_climatology_1959_1992.csv")
    if not df.empty and "station_name" in df.columns:
        df = df[~df["station_name"].astype(str).str.startswith("~$")]
    return df


@st.cache_data(show_spinner=False)
def load_caucasus_metadata(_ver: str = _DATA_CACHE_VERSION) -> pd.DataFrame:
    df = _read_csv(CAUCASUS / "derived" / "station_metadata.csv")
    if not df.empty:
        df = df[~df["station_name"].astype(str).str.startswith("~$")].drop_duplicates(
            subset=["station_id"], keep="first"
        )
    return df


def caucasus_completeness_summary_path() -> Path:
    return (
        CAUCASUS
        / "derived"
        / "completeness_audit_1959_1992"
        / "caucasus_station_completeness_summary_1959_1992.csv"
    )


def load_caucasus_completeness_summary() -> pd.DataFrame:
    """Not cached: empty result when the file was missing should not be cached forever."""
    return _read_csv(caucasus_completeness_summary_path())


@st.cache_data(show_spinner=False)
def load_senamhi_annual_lr(window: str, _ver: str = _DATA_CACHE_VERSION) -> pd.DataFrame:
    name = "senamhi_annual_lapse_rate_1967_1992.csv" if window == "historical" else "senamhi_annual_lapse_rate_2004_2019.csv"
    return _read_csv(SENAMHI / "derived" / name)


@st.cache_data(show_spinner=False)
def load_senamhi_seasonal_long(window: str, relaxed: bool = True, _ver: str = _DATA_CACHE_VERSION) -> pd.DataFrame:
    if window == "historical":
        fname = (
            "senamhi_seasonal_lapse_rate_long_1967_1992_relaxed_sf50_m3of4.csv"
            if relaxed
            else "senamhi_seasonal_lapse_rate_long_1967_1992.csv"
        )
    else:
        fname = (
            "senamhi_seasonal_lapse_rate_long_2004_2019_relaxed_sf67_m3of4.csv"
            if relaxed
            else "senamhi_seasonal_lapse_rate_long_2004_2019.csv"
        )
    return _read_csv(SENAMHI / "derived" / fname)


@st.cache_data(show_spinner=False)
def load_senamhi_fl(variant: str, _ver: str = _DATA_CACHE_VERSION) -> pd.DataFrame:
    mapping = {
        "sf33": "senamhi_freezing_level_timeseries_1967_1992_sf33.csv",
        "sf50": "senamhi_freezing_level_timeseries_1967_1992_sf50.csv",
        "sf67": "senamhi_freezing_level_timeseries_2004_2019_sf67.csv",
    }
    return _read_csv(SENAMHI / "derived" / mapping.get(variant, mapping["sf33"]))


@st.cache_data(show_spinner=False)
def load_senamhi_fl_fixedpair(_ver: str = _DATA_CACHE_VERSION) -> pd.DataFrame:
    path = (
        SENAMHI
        / "FL_timeseries_v2"
        / "senamhi_freezing_level_timeseries_v2_fixedpair_cajatambo_chavin_1994_2019.csv"
    )
    return _read_csv(path)


@st.cache_data(show_spinner=False)
def load_lascar_seasonal(relaxed: bool = False, _ver: str = _DATA_CACHE_VERSION) -> pd.DataFrame:
    fname = (
        "lascar_seasonal_lr_timeseries_relaxed_2006_2025.csv"
        if relaxed
        else "lascar_seasonal_lr_timeseries_2006_2025.csv"
    )
    return _read_csv(LASCAR / "seasonal_lr_analysis" / fname)


@st.cache_data(show_spinner=False)
def load_senamhi_station_sample(_ver: str = _DATA_CACHE_VERSION) -> pd.DataFrame:
    """One row per station for the map (bundled slim CSV or from daily_clean)."""
    slim = SENAMHI / "derived" / "senamhi_stations_map.csv"
    if slim.is_file():
        df = pd.read_csv(slim)
        if {"station_name", "latitude", "longitude"}.issubset(df.columns):
            return df.rename(columns={"station_name": "station"}).rename(
                columns={"latitude": "lat", "longitude": "lon"}
            )
    derived = SENAMHI / "derived"
    rows = []
    for p in sorted(derived.glob("*_daily_clean.csv")):
        try:
            head = pd.read_csv(p, nrows=1)
        except Exception:
            continue
        if {"latitude", "longitude", "elevation_m", "station_name"}.issubset(head.columns):
            rows.append(
                {
                    "station": head["station_name"].iloc[0],
                    "lat": head["latitude"].iloc[0],
                    "lon": head["longitude"].iloc[0],
                    "elevation_m": head["elevation_m"].iloc[0],
                }
            )
    return pd.DataFrame(rows)
