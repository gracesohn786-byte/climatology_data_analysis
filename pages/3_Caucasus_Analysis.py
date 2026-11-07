"""Caucasus lapse rate and freezing level — centerpiece section."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bootstrap import ensure_streamlit_path  # noqa: E402

APP_DIR = ensure_streamlit_path()

from components import charts, metrics  # noqa: E402
from components.layout import img_kwargs, plotly_kwargs  # noqa: E402
from components.data_loaders import (  # noqa: E402
    load_caucasus_annual_lr,
    load_caucasus_climatology,
    load_caucasus_fl,
    load_caucasus_seasonal_lr_long,
    load_caucasus_seasonal_diag,
)
from components.paths import (  # noqa: E402
    REPO_ROOT,
    caucasus_completeness_heatmap_pngs,
    caucasus_png_annual_lr,
    caucasus_png_climatology_scatter,
    caucasus_png_freezing_level,
    caucasus_png_seasonal_lr_main,
    caucasus_png_seasonal_lr_old,
)
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

if annual.empty or "year" not in annual.columns:
    st.error(
        "Caucasus **analysis CSVs are missing** from this deployment. "
        "Commit **`caucasus_annual_lapse_rate_timeseries_1959_1992.csv`** under either "
        "`Caucasus_Weather_Stations/derived/` (recommended) or **`Caucasus_Weather_Stations/`** at repo root, "
        "or use the bundled copy under `streamlit_app/data/Caucasus_Weather_Stations/derived/`. "
        f"Paths resolve from clone root `{REPO_ROOT}` (folder `Caucasus_Weather_Stations` must live there)."
    )

tabs = st.tabs(["Overview", "Annual LR", "Seasonal LR", "Freezing level", "Climatology", "Completeness"])

with tabs[0]:
    c1, c2, c3 = st.columns(3)
    if not annual.empty and "lr_climatology" in annual.columns:
        c1.metric("Mean annual LR", f"{annual['lr_climatology'].iloc[0]:.2f} °C/km")
        c2.metric("σ (annual LR)", f"{annual['lr_sigma'].iloc[0]:.2f} °C/km")
    valid_season = (
        seasonal[seasonal["lapse_rate"].notna()]["year"].nunique()
        if not seasonal.empty and "year" in seasonal.columns
        else 0
    )
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
    if annual.empty or "year" not in annual.columns:
        st.warning("Load annual lapse rate CSV to enable this tab.")
    else:
        y0, y1 = year_range_slider("Annual LR year range", 1959, 1992, "cauc_annual_yr")
        show_trend = st.checkbox("Show linear trend line", value=True, key="cauc_ann_trend")
        metrics.metric_row_lr(annual[(annual["year"] >= y0) & (annual["year"] <= y1)])
        st.plotly_chart(charts.fig_annual_lr(annual, y0, y1, show_trend), **plotly_kwargs())
        st.plotly_chart(charts.fig_r2_timeseries(annual, y0, y1), **plotly_kwargs())
        show_static_expander(
            "Original research figure — annual LR",
            caucasus_png_annual_lr(),
            "Annual lapse rate with OLS trend (1959–1992). Source: annual_LR_analysis.",
        )

with tabs[2]:
    if seasonal.empty or "year" not in seasonal.columns:
        st.warning("Load seasonal lapse rate CSV to enable this tab.")
    else:
        y0, y1 = year_range_slider("Seasonal LR year range", 1959, 1992, "cauc_seas_yr")
        ylim_choice = st.radio("Y-axis", ["Auto", "4–8 °C/km (poster view)"], horizontal=True, key="cauc_ylim")
        ylim = (4.0, 8.0) if "4–8" in ylim_choice else None
        show_tr = st.checkbox("Show per-season OLS trends", value=False, key="cauc_seas_tr")
        sub = seasonal[(seasonal["year"] >= y0) & (seasonal["year"] <= y1)]
        metrics.metric_seasonal_means(sub)
        st.plotly_chart(
            charts.fig_seasonal_lr(seasonal, y0, y1, ylim=ylim, show_trend=show_tr), **plotly_kwargs()
        )
        if not diag.empty and "year" in diag.columns:
            with st.expander("Diagnostics (1992 excluded: station_count)"):
                st.dataframe(diag[["year", "notes", "n_stations_used", "warm_months", "cool_months"]], hide_index=True)
        show_static_expander(
            "Original figure (y-axis 4–8)",
            caucasus_png_seasonal_lr_main(),
            "Warm (red) vs cool (blue) seasonal LR, 1959–1992.",
        )
        show_static_expander(
            "Original figure (auto y-axis)",
            caucasus_png_seasonal_lr_old(),
            "Earlier export before fixed y-axis limits.",
        )

with tabs[3]:
    if fl.empty or "year" not in fl.columns:
        st.warning("Load freezing level CSV to enable this tab.")
    else:
        y0, y1 = year_range_slider("Freezing level year range", 1959, 1992, "cauc_fl_yr")
        show_ci = st.checkbox("Show 95% bootstrap CI", value=True, key="cauc_fl_ci")
        metrics.metric_fl(fl[(fl["year"] >= y0) & (fl["year"] <= y1)])
        st.plotly_chart(charts.fig_freezing_level(fl, y0, y1, show_ci=show_ci), **plotly_kwargs())
        st.caption(
            "FL is interpolated within the network elevation range (all years `fl_within_range=True`). "
            "Wide CI in late 1980s–1992 reflects fewer active stations."
        )
        show_static_expander(
            "Original research figure — freezing level",
            caucasus_png_freezing_level(),
            "Annual FL, bootstrap band, linear trend.",
        )

with tabs[4]:
    need = {"elevation_m", "station_name", "tmean_c_clim", "tmax_c_clim", "tmin_c_clim"}
    if clim.empty or not need.issubset(set(clim.columns)):
        st.warning("Load climatology CSV (`caucasus_station_annual_climatology_1959_1992.csv`) to enable this tab.")
    else:
        options = [
            ("tmean_c_clim", "Mean daily (monthly mean of daily mean)"),
            ("tmax_c_clim", "Daytime proxy (Tmax)"),
            ("tmin_c_clim", "Nighttime proxy (Tmin)"),
        ]
        choice = st.selectbox("Temperature series", options, format_func=lambda x: x[1])
        temp_col, label = choice
        st.plotly_chart(charts.fig_climatology_scatter(clim, temp_col, label), **plotly_kwargs())
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
        caucasus_png_climatology_scatter(),
        "Elevation vs temperature climatology scatter with regression table.",
    )

with tabs[5]:
    st.markdown("Per-station monthly availability heatmaps (1959–1992 common period).")
    heat_pngs = caucasus_completeness_heatmap_pngs()
    if not heat_pngs:
        st.info(
            "Heatmap PNGs not found in this deployment. Commit "
            "`streamlit_app/data/Caucasus_Weather_Stations/completeness_audit/` "
            "(from `python streamlit_app/scripts/bundle_data.py`) or include "
            "`Caucasus_Weather_Stations/completeness_audit/monthly_grids_1959-1992_(missing_data)/` "
            "in the GitHub repo."
        )
    for p in heat_pngs:
        label = (
            p.stem.replace("_monthly_clean_availability_heatmap_1959_1992", "")
            .replace("_availability_heatmap_1959_1992", "")
            .replace("_", " ")
            .title()
        )
        with st.expander(label):
            st.image(str(p), **img_kwargs())
