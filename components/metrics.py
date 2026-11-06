"""Display summary metrics from analysis DataFrames."""
from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st


def metric_row_lr(df: pd.DataFrame, lr_col: str = "lapse_rate") -> None:
    if df.empty or lr_col not in df.columns or "year" not in df.columns:
        st.warning("Lapse rate data not available.")
        return
    s = df[lr_col].dropna()
    if s.empty:
        st.warning("No finite lapse rate values.")
        return
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mean LR", f"{s.mean():.3f} °C/km")
    c2.metric("σ", f"{s.std():.3f} °C/km")
    i_min = df[lr_col].idxmin()
    i_max = df[lr_col].idxmax()
    c3.metric("Min (year)", f"{df.loc[i_min, lr_col]:.3f} ({int(df.loc[i_min, 'year'])})")
    c4.metric("Max (year)", f"{df.loc[i_max, lr_col]:.3f} ({int(df.loc[i_max, 'year'])})")


def metric_seasonal_means(long_df: pd.DataFrame) -> None:
    if long_df.empty:
        return
    warm = long_df[long_df["season"] == "warm"]["lapse_rate"].dropna()
    cool = long_df[long_df["season"] == "cool"]["lapse_rate"].dropna()
    c1, c2, c3 = st.columns(3)
    if not warm.empty:
        c1.metric("Warm mean LR", f"{warm.mean():.2f} °C/km", help=f"n = {len(warm)} years")
    if not cool.empty:
        c2.metric("Cool mean LR", f"{cool.mean():.2f} °C/km", help=f"n = {len(cool)} years")
    if not warm.empty and not cool.empty:
        c3.metric("Cool − warm (mean)", f"{cool.mean() - warm.mean():.2f} °C/km")


def metric_fl(df: pd.DataFrame) -> None:
    if df.empty or "freezing_level_m" not in df.columns:
        return
    fl = df["freezing_level_m"].dropna()
    if fl.empty:
        return
    c1, c2, c3 = st.columns(3)
    c1.metric("Mean FL", f"{fl.mean():.0f} m")
    c2.metric("Range", f"{fl.min():.0f} – {fl.max():.0f} m")
    if "fl_trend_slope_m_per_yr" in df.columns:
        slope = df["fl_trend_slope_m_per_yr"].dropna()
        if not slope.empty:
            c3.metric("Trend slope", f"{slope.iloc[0]:.2f} m/yr", help="Descriptive OLS on FL vs year")


def trend_slope_lr(df: pd.DataFrame, lr_col: str = "lapse_rate") -> float | None:
    if df.empty or lr_col not in df.columns:
        return None
    sub = df[["year", lr_col]].dropna()
    if len(sub) < 2:
        return None
    coef = np.polyfit(sub["year"].astype(float), sub[lr_col].astype(float), 1)
    return float(coef[0])
