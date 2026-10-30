"""Research overview and networks."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from components.data_loaders import load_caucasus_metadata, load_senamhi_station_sample  # noqa: E402
from components.poster_text import extract_abstract  # noqa: E402
from components.paths import POSTER_PDF  # noqa: E402

st.set_page_config(page_title="Research Overview", layout="wide")
st.title("Research Overview")

st.markdown(
    """
### Background: Elevation-Dependent Warming (EDW)

High-elevation environments often warm at different rates than low elevations. Detecting EDW requires
consistent temperature records along elevation gradients. **Network lapse rates**—slopes from regressing
station elevation on mean temperature—provide a compact diagnostic of vertical thermal structure and how
it changes **annually** and **seasonally**.

### Objectives

1. Quantify **annual** and **seasonal** (warm vs cool) lapse rates for the Caucasus (1959–1992) and Peru networks.
2. Estimate **freezing level** (0 °C isotherm altitude) where the station network brackets 0 °C (Caucasus).
3. Document **data completeness**, quality rules, and limitations of cross-station regression.
4. Compare Caucasus and Peru magnitudes and variability (historical overlap 1967–1991 where applicable).
"""
)

extract_path = APP_DIR / "assets" / "poster_extract.txt"
abstract = extract_abstract(extract_path)
if abstract:
    st.subheader("Abstract (STARS 2026 poster)")
    st.markdown(abstract)
elif POSTER_PDF.is_file():
    st.caption("Poster PDF is available; run `python streamlit_app/scripts/extract_poster_text.py` to populate the abstract.")

st.subheader("Station networks")

tab_c, tab_p = st.tabs(["Caucasus (8 stations)", "Peru SENAMHI (sample map)"])

with tab_c:
    meta = load_caucasus_metadata()
    if meta.empty:
        st.warning("Caucasus metadata not found.")
    else:
        st.dataframe(
            meta[["station_name", "elevation_m", "latitude", "longitude"]].sort_values("elevation_m"),
            use_container_width=True,
            hide_index=True,
        )
        map_df = meta.rename(columns={"latitude": "lat", "longitude": "lon"})
        st.map(map_df[["lat", "lon"]], size=20)

with tab_p:
    st.markdown(
        """
**Historical window (1967–1992):** Group A — nine nominal stations (coastal to high Andes).  
**Modern window (2004–2019):** Group C — up to fourteen stations.  
**Lascar EDW transect (2006–2025):** five loggers from ~3955–4760 m (seasonal LR only in this app).
        """
    )
    sen = load_senamhi_station_sample()
    if not sen.empty:
        st.dataframe(sen.sort_values("elevation_m"), use_container_width=True, hide_index=True)
        st.map(sen.rename(columns={"lat": "lat", "lon": "lon"}), size=15)

st.subheader("Why this matters")

st.markdown(
    """
- **Lapse rate** controls how strongly temperature falls with height; seasonal differences can signal EDW-style contrasts.
- **Freezing level** sets rain/snow partitioning and glacier accumulation zones where it is **within** the network range.
- Rigorous **missing-data rules** (month/day thresholds, station fractions) ensure reported slopes are not artifacts of sparse coverage.
"""
)
