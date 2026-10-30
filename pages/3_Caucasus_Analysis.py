"""Caucasus lapse rate and freezing level — centerpiece section."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from components import charts, metrics  # noqa: E402
from components.data_loaders import (  # noqa: E402
    load_caucasus_annual_lr,
    load_caucasus_climatology,
    load_caucasus_fl,
    load_caucasus_seasonal_lr_long,
    load_caucasus_seasonal_diag,
)
from components.paths import CAUCASUS  # noqa: E402
from components.sidebar import year_range_slider  # noqa: E402
from components.static_figures import show_static_expander  # noqa: E402

st.set_page_config(page_title="Caucasus Analysis", layout="wide")
st.title("Caucasus Analysis (1959–1992)")

st.markdown(
    """
Eight stations in the western Greater Caucasus (118–2854 m). This section mirrors the **STARS 2026** poster:
annual LR, seasonal warm/cool LR, freezing level with bootstrap uncertainty, and climatological cross-sections.
**1992** seasonal LR is excluded (station count below 75% threshold).
"""
)

annual = load_caucasus_annual_lr()
seasonal = load_caucasus_seasonal_lr_long()
fl = load_caucasus_fl()
clim = load_caucasus_climatology()
diag = load_caucasus_seasonal_diag()

tabs = st.tabs(["Overview", "Annual LR", "Seasonal LR", "Freezing level", "Climatology", "Completeness"])

with tabs[0]:
    c1, c2, c3 = st.columns(3)
    if not annual.empty and "lr_climatology" in annual.columns:
        c1.metric("Mean annual LR", f"{annual['lr_climatology'].iloc[0]:.2f} °C/km")
        c2.metric("σ (annual LR)", f"{annual['lr_sigma'].iloc[0]:.2f} °C/km")
    valid_season = seasonal[seasonal["lapse_rate"].notna()]["year"].nunique() if not seasonal.empty else 0
    c3.metric("Seasonal valid years", f"{valid_season}", help="Years with ok warm/cool LR")
    st.markdown(
        """
**Key findings (from analysis reports):**
- Cool-season LR **exceeds** warm-season LR in most years (mean ~6.13 vs ~5.74 °C/km, 1959–1991).
- **Widening warm/cool gap** after ~1975; cool-season peaks in **1987–1989** (~6.9–7.0 °C/km).
- Annual spatial **R² > 0.98** every year; FL trend **≈ −2.18 m/yr** (descriptive OLS, 34 years).
        """
    )

with tabs[1]:
    y0, y1 = year_range_slider("Annual LR year range", 1959, 1992, "cauc_annual_yr")
    show_trend = st.checkbox("Show linear trend line", value=True, key="cauc_ann_trend")
    metrics.metric_row_lr(annual[(annual["year"] >= y0) & (annual["year"] <= y1)])
    st.plotly_chart(charts.fig_annual_lr(annual, y0, y1, show_trend), use_container_width=True)
    st.plotly_chart(charts.fig_r2_timeseries(annual, y0, y1), use_container_width=True)
    show_static_expander(
        "Original research figure — annual LR",
        CAUCASUS / "annual_LR_analysis" / "caucasus_annual_lapse_rate_timeseries_1959_1992.png",
        "Annual lapse rate with OLS trend (1959–1992). Source: annual_LR_analysis.",
    )

with tabs[2]:
    y0, y1 = year_range_slider("Seasonal LR year range", 1959, 1992, "cauc_seas_yr")
    ylim_choice = st.radio("Y-axis", ["Auto", "4–8 °C/km (poster view)"], horizontal=True, key="cauc_ylim")
    ylim = (4.0, 8.0) if "4–8" in ylim_choice else None
    show_tr = st.checkbox("Show per-season OLS trends", value=False, key="cauc_seas_tr")
    sub = seasonal[(seasonal["year"] >= y0) & (seasonal["year"] <= y1)]
    metrics.metric_seasonal_means(sub)
    st.plotly_chart(charts.fig_seasonal_lr(seasonal, y0, y1, ylim=ylim, show_trend=show_tr), use_container_width=True)
    if not diag.empty:
        with st.expander("Diagnostics (1992 excluded: station_count)"):
            st.dataframe(diag[["year", "notes", "n_stations_used", "warm_months", "cool_months"]], hide_index=True)
    show_static_expander(
        "Original figure (y-axis 4–8)",
        CAUCASUS / "seasonal_LR_analysis" / "caucasus_seasonal_lapse_rate_timeseries_1959_1992.png",
        "Warm (red) vs cool (blue) seasonal LR, 1959–1992.",
    )
    show_static_expander(
        "Original figure (auto y-axis)",
        CAUCASUS / "seasonal_LR_analysis" / "caucasus_seasonal_lapse_rate_timeseries_1959_1992_old.png",
        "Earlier export before fixed y-axis limits.",
    )

with tabs[3]:
    y0, y1 = year_range_slider("Freezing level year range", 1959, 1992, "cauc_fl_yr")
    show_ci = st.checkbox("Show 95% bootstrap CI", value=True, key="cauc_fl_ci")
    metrics.metric_fl(fl[(fl["year"] >= y0) & (fl["year"] <= y1)])
    st.plotly_chart(charts.fig_freezing_level(fl, y0, y1, show_ci=show_ci), use_container_width=True)
    st.caption(
        "FL is interpolated within the network elevation range (all years `fl_within_range=True`). "
        "Wide CI in late 1980s–1992 reflects fewer active stations."
    )
    show_static_expander(
        "Original research figure — freezing level",
        CAUCASUS / "FL_timeseries_analysis" / "caucasus_freezing_level_timeseries_1959_1992.png",
        "Annual FL, bootstrap band, linear trend.",
    )

with tabs[4]:
    options = [
        ("tmean_c_clim", "Mean daily (monthly mean of daily mean)"),
        ("tmax_c_clim", "Daytime proxy (Tmax)"),
        ("tmin_c_clim", "Nighttime proxy (Tmin)"),
    ]
    choice = st.selectbox("Temperature series", options, format_func=lambda x: x[1])
    temp_col, label = choice
    st.plotly_chart(charts.fig_climatology_scatter(clim, temp_col, label), use_container_width=True)
    st.markdown(
        """
| Series | LR (°C/km) | FL (m) — from climatology report |
|--------|------------|----------------------------------|
| Mean daily | 5.79 | 2453 |
| Daytime (Tmax) | 6.67 | 3150 |
| Nighttime (Tmin) | 5.40 | 1784 |

Daytime shows the steepest LR and highest FL; nighttime the weakest LR and lowest FL.
Tmax/Tmin are **proxies**, not fixed solar-hour day/night samples.
        """
    )
    show_static_expander(
        "Original climatology figure",
        CAUCASUS
        / "LR_Elevation_vs_Temp_Analysis"
        / "plot"
        / "caucasus_lapse_rate_climatology_elevation_vs_temp_1959_1992.png",
        "Elevation vs temperature climatology scatter with regression table.",
    )

with tabs[5]:
    st.markdown("Per-station monthly availability heatmaps (1959–1992 common period).")
    heat_dir = CAUCASUS / "completeness_audit" / "monthly_grids_1959-1992_(missing_data)"
    for p in sorted(heat_dir.glob("*_1959_1992.png")) if heat_dir.is_dir() else []:
        with st.expander(p.stem.replace("_availability_heatmap_1959_1992", "").replace("_", " ").title()):
            st.image(str(p), use_container_width=True)
