"""Weather station lapse rate & freezing level — research presentation (home)."""
from __future__ import annotations

import streamlit as st

from bootstrap import ensure_streamlit_path  # noqa: E402

APP_DIR = ensure_streamlit_path()

from components.layout import img_kwargs  # noqa: E402
from components.paths import POSTER_PDF, POSTER_PREVIEW  # noqa: E402

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

st.subheader("STARS 2026 poster")
poster_col, dl_col = st.columns([4, 1])
with dl_col:
    if POSTER_PDF.is_file():
        st.download_button(
            label="Download PDF",
            data=POSTER_PDF.read_bytes(),
            file_name="Stars_2026_poster.pdf",
            mime="application/pdf",
            type="primary",
        )
    else:
        st.caption("PDF not found in `poster/`.")

if POSTER_PREVIEW.is_file():
    st.image(
        str(POSTER_PREVIEW),
        caption="STARS 2026 research poster (preview).",
        **img_kwargs(),
    )
elif POSTER_PDF.is_file():
    st.info(
        "Poster preview image missing. Run "
        "`python streamlit_app/scripts/render_poster_preview.py` locally, commit "
        "`streamlit_app/poster/Stars_2026_poster_preview.png`, then redeploy."
    )
else:
    st.info("Poster PDF and preview not found under `poster/`.")

st.divider()

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

st.divider()
st.markdown(
    """
**Data integrity:** All numbers in interactive charts are loaded from existing derived CSVs in this repository.
Original publication-style PNGs are preserved under each analysis folder and shown in expanders where noted.
"""
)
