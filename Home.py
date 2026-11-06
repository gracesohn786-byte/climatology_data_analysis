"""Weather station lapse rate & freezing level — research presentation (home)."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

from bootstrap import ensure_streamlit_path  # noqa: E402

APP_DIR = ensure_streamlit_path()

from components.paths import POSTER_PDF  # noqa: E402

st.set_page_config(
    page_title="Mountain Lapse Rates & EDW",
    page_icon="⛰",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Elevation-Dependent Warming and Lapse Rates in Mountain Networks")
st.markdown(
    """
This interactive presentation summarizes **cross-station regression analyses** of lapse rate (LR)
and freezing level (FL) for the **western Greater Caucasus** (1959–1992) and **Peruvian Andes**
(SENAMHI and Lascar EDW transect). The Caucasus results are the focus of the **STARS 2026** poster.
"""
)

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Research focus")
    st.markdown(
        """
- **Scientific question:** How does the temperature–elevation relationship (lapse rate) vary in time and
  between warm vs cool seasons, and what does that imply for **Elevation-Dependent Warming (EDW)** and
  freezing-level altitude?
- **Method:** For each year (or season), fit **elevation = m × T + b** across stations; **LR = −1000/m** (°C/km),
  **FL = b** (m at T = 0 °C). This is a **horizontal network** fit, not a single vertical atmospheric profile.
- **Navigate** using the sidebar: Overview → Data & Methods → **Caucasus Analysis** → Peru → Regional Comparison → Conclusions.
        """
    )
with col2:
    st.subheader("Poster reference")
    if POSTER_PDF.is_file():
        st.caption(f"STARS 2026 poster: `{POSTER_PDF.relative_to(APP_DIR)}`")
        with open(POSTER_PDF, "rb") as f:
            st.download_button(
                label="Download poster (PDF)",
                data=f.read(),
                file_name="Stars_2026_poster.pdf",
                mime="application/pdf",
            )
    else:
        st.info("Poster PDF not found in `poster/`.")

st.divider()
st.markdown(
    """
**Data integrity:** All numbers in interactive charts are loaded from existing derived CSVs in this repository.
Original publication-style PNGs are preserved under each analysis folder and shown in expanders where noted.
"""
)
