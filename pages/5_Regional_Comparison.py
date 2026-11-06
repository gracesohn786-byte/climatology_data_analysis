"""Caucasus vs Peru historical comparison."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bootstrap import ensure_streamlit_path  # noqa: E402

ensure_streamlit_path()

from components.data_loaders import load_caucasus_annual_lr, load_senamhi_annual_lr  # noqa: E402
from components.layout import df_kwargs  # noqa: E402
from components.paths import senamhi_comparison_writeup_paths, senamhi_png_fl_comparison_caucasus  # noqa: E402
from components.static_figures import show_static  # noqa: E402

st.set_page_config(page_title="Regional Comparison", layout="wide")
st.title("Regional Comparison — Caucasus vs SENAMHI (Historical)")

st.markdown(
    """
Shared **method:** annual mean temperature per station → OLS **z = mT + b** → LR = −1000/m, FL = b.  
Overlap for context: **1967–1991** (1987 missing in SENAMHI; 1992 not in SENAMHI historical end).  
Trends below are **descriptive OLS**; not tests of statistical significance.
"""
)

cauc = load_caucasus_annual_lr()
sen = load_senamhi_annual_lr("historical")

if cauc.empty or sen.empty:
    st.error("Comparison CSVs missing.")
else:
    c_mean = cauc["lapse_rate"].mean()
    c_std = cauc["lapse_rate"].std()
    s_mean = sen["lapse_rate"].mean()
    s_std = sen["lapse_rate"].std()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Caucasus mean LR", f"{c_mean:.2f} °C/km", "1959–1992")
    m2.metric("SENAMHI mean LR", f"{s_mean:.2f} °C/km", "1967–1992")
    m3.metric("Caucasus σ", f"{c_std:.2f} °C/km")
    m4.metric("SENAMHI σ", f"{s_std:.2f} °C/km")

    comp = pd.DataFrame(
        [
            {"Aspect": "Mean LR (°C/km)", "Caucasus": "~5.83", "SENAMHI historical": "~3.22"},
            {"Aspect": "CV (approx.)", "Caucasus": "~3.1%", "SENAMHI historical": "~7.4%"},
            {"Aspect": "Typical R²", "Caucasus": "> 0.98", "SENAMHI historical": "0.73 – 1.00"},
            {"Aspect": "FL interpretable?", "Caucasus": "Yes (within network)", "SENAMHI historical": "No (extrapolation)"},
            {"Aspect": "LR trend (descriptive)", "Caucasus": "Slight rise", "SENAMHI historical": "Slight fall"},
        ]
    )
    st.dataframe(comp, hide_index=True, **df_kwargs())

st.subheader("Structural differences")
st.markdown(
    """
- **Magnitude:** Caucasus LR ~1.8× SENAMHI — mid-latitude cold pooling vs compressed tropical gradient.
- **Variability:** SENAMHI proportionally noisier (sparse network, 3–7 stations/year).
- **Freezing level:** Only Caucasus FL is geophysically bracketed by stations straddling 0 °C (Mamisoni Pass ~ −2 °C annual mean).
- **Shared anomaly example:** **1986** — both networks show below-normal LR; **1971** low LR is Caucasus-specific.
"""
)

st.subheader("Comparison figure")
show_static(
    senamhi_png_fl_comparison_caucasus(),
    "Freezing level / trend comparison plot (note SENAMHI extrapolation caveat).",
)

with st.expander("Full comparison write-ups (repository markdown)"):
    writeups = senamhi_comparison_writeup_paths()
    if not writeups:
        st.info(
            "Comparison markdown not found. After pulling the latest app, commit "
            "`streamlit_app/data/Senamhi_Weather_Stations/.../*.md` (from `python streamlit_app/scripts/bundle_data.py`) "
            "or include `Senamhi_Weather_Stations/` in the GitHub repo linked to Streamlit."
        )
    for path in writeups:
        st.markdown(f"**{path.name}**")
        st.markdown(path.read_text(encoding="utf-8", errors="replace")[:12000])
