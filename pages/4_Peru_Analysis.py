"""Peru: SENAMHI and Lascar EDW analyses."""
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
    load_lascar_seasonal,
    load_senamhi_annual_lr,
    load_senamhi_fl,
    load_senamhi_fl_fixedpair,
    load_senamhi_seasonal_long,
)
from components.paths import (  # noqa: E402
    LASCAR,
    SENAMHI,
    lascar_png_seasonal_timeseries,
    senamhi_png_annual_lr,
    senamhi_png_freezing_level_fixedpair_cajatambo_chavin,
    senamhi_png_freezing_level_sf33,
    senamhi_png_freezing_level_sf50,
    senamhi_png_freezing_level_sf67,
    senamhi_png_seasonal_lr_relaxed,
)
from components.sidebar import year_range_slider  # noqa: E402
from components.static_figures import show_static_expander  # noqa: E402

st.set_page_config(page_title="Peru Analysis", layout="wide")
st.title("Peru Analysis — SENAMHI & Lascar EDW")

st.warning(
    "**Freezing level (network-wide SENAMHI):** Annual mean temperatures at all stations are typically **> 0 °C**. "
    "The regression intercept (FL) is an **extrapolation** above the highest station—not an observed 0 °C altitude. "
    "Do not interpret those values as measured freezing levels. The **Cajatambo–Chavin fixed-pair** series is a "
    "two-station diagnostic only."
)

tabs = st.tabs(["Networks & coverage", "Annual LR", "Seasonal LR", "Freezing level", "Lascar transect"])

with tabs[0]:
    st.markdown(
        """
**Historical (1967–1992):** Group A — sparse coverage; many years with 3–7 stations.  
**Modern (2004–2019):** Group C — 12–14 stations most years.  
**Lascar:** Five loggers, 3955–4760 m, seasonal LR 2006–2025.
        """
    )
    miss = SENAMHI / "missing_months"
    pngs = sorted(miss.glob("*_availability_heatmap.png")) if miss.is_dir() else []
    if pngs:
        pick = st.selectbox("SENAMHI daily→monthly availability", [p.name for p in pngs])
        st.image(str(miss / pick), **img_kwargs())

with tabs[1]:
    window = st.radio("Window", ["historical", "modern"], horizontal=True, format_func=lambda w: "1967–1992" if w == "historical" else "2004–2019")
    df = load_senamhi_annual_lr(window)
    if df.empty:
        st.error("Annual LR CSV missing.")
    else:
        y0, y1 = int(df["year"].min()), int(df["year"].max())
        yr = year_range_slider("Annual LR year range", y0, y1, f"sen_ann_{window}")
        metrics.metric_row_lr(df[(df["year"] >= yr[0]) & (df["year"] <= yr[1])])
        slope = metrics.trend_slope_lr(df)
        if slope is not None:
            st.caption(f"Descriptive OLS slope (full series): {slope:.5f} °C/km per year")
        st.plotly_chart(charts.fig_annual_lr(df, yr[0], yr[1], True), **plotly_kwargs())
        show_static_expander(
            "Original figure",
            senamhi_png_annual_lr(window == "historical"),
            "SENAMHI annual LR time series.",
        )

with tabs[2]:
    window = st.radio("Window ", ["historical", "modern"], horizontal=True, key="seas_w", format_func=lambda w: "1967–1992 (sf50, 3/4 mo)" if w == "historical" else "2004–2019 (sf67, 3/4 mo)")
    long_df = load_senamhi_seasonal_long(window, relaxed=True)
    if long_df.empty:
        st.error("Seasonal CSV missing.")
    else:
        y0, y1 = int(long_df["year"].min()), int(long_df["year"].max())
        yr = year_range_slider("Seasonal LR year range", y0, y1, f"sen_seas_{window}")
        sub = long_df[(long_df["year"] >= yr[0]) & (long_df["year"] <= yr[1])]
        metrics.metric_seasonal_means(sub)
        st.plotly_chart(charts.fig_seasonal_lr(long_df, yr[0], yr[1], show_trend=True), **plotly_kwargs())
        show_static_expander(
            "Original figure",
            senamhi_png_seasonal_lr_relaxed(window == "historical"),
            "Relaxed quality rules documented in seasonal_LR_analysis.md.",
        )

with tabs[3]:
    variant = st.selectbox(
        "SENAMHI FL variant",
        [
            ("sf33", "Historical 1967–1992 (≥3 stations, visualization)"),
            ("sf50", "Historical strict (≥5 stations, sparse)"),
            ("sf67", "Modern 2004–2019 (≥10 stations)"),
            ("fixedpair", "Fixed pair Cajatambo–Chavin 1994–2019"),
        ],
        format_func=lambda x: x[1],
    )
    key = variant[0]
    if key == "fixedpair":
        df = load_senamhi_fl_fixedpair()
        st.info("Two-station regression; FL often outside station elevation range—extrapolation flag applies.")
    else:
        df = load_senamhi_fl(key)
    if df.empty:
        st.error("FL CSV not found.")
    else:
        y0, y1 = int(df["year"].min()), int(df["year"].max())
        yr = year_range_slider("Freezing level year range", y0, y1, f"sen_fl_{key}")
        fl_col = "freezing_level_m" if "freezing_level_m" in df.columns else "fl_m"
        if fl_col in df.columns:
            df = df.rename(columns={fl_col: "freezing_level_m"})
        has_ci = {"fl_ci_lo", "fl_ci_hi"}.issubset(df.columns)
        st.plotly_chart(charts.fig_freezing_level(df, yr[0], yr[1], show_ci=has_ci), **plotly_kwargs())
        if key == "sf33":
            show_static_expander(
                "Original figure",
                senamhi_png_freezing_level_sf33(),
                "Historical FL (extrapolation)—for method comparison only.",
            )
        elif key == "sf67":
            show_static_expander(
                "Original figure",
                senamhi_png_freezing_level_sf67(),
                "Modern window FL series.",
            )
        elif key == "sf50":
            show_static_expander(
                "Original figure",
                senamhi_png_freezing_level_sf50(),
                "Historical strict network (≥5 stations)—often sparse years.",
            )
        elif key == "fixedpair":
            show_static_expander(
                "Original figure — fixed pair",
                senamhi_png_freezing_level_fixedpair_cajatambo_chavin(),
                "Cajatambo–Chavin fixed-pair FL (v2 export).",
            )

with tabs[4]:
    relaxed = st.checkbox("Relaxed station-fraction run", value=False, key="lascar_relax")
    ldf = load_lascar_seasonal(relaxed=relaxed)
    st.markdown("High-elevation transect; strict run uses station-fraction gate (13/20 valid years); relaxed adds 2012, 2015.")
    if ldf.empty:
        st.error("Lascar seasonal CSV missing.")
    else:
        y0, y1 = 2006, 2025
        yr = year_range_slider("Lascar seasonal year range", y0, y1, "lascar_yr")
        metrics.metric_seasonal_means(ldf[(ldf["year"] >= yr[0]) & (ldf["year"] <= yr[1])])
        st.plotly_chart(charts.fig_seasonal_lr(ldf, yr[0], yr[1]), **plotly_kwargs())
        show_static_expander(
            "Original figure",
            lascar_png_seasonal_timeseries(relaxed),
            "Lascar seasonal warm vs cool LR.",
        )
        for station in ["llanup1", "llanup2", "llanup3", "llanup4", "llanport"]:
            hp = LASCAR / "seasonal_lr_analysis" / f"completeness_heatmap_{station}.png"
            if hp.is_file():
                with st.expander(f"Completeness — {station}"):
                    st.image(str(hp), **img_kwargs())
