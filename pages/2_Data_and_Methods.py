"""Data sources, cleaning, and regression methodology."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from components.data_loaders import (  # noqa: E402
    caucasus_completeness_summary_path,
    load_caucasus_completeness_summary,
)
from components.paths import CAUCASUS  # noqa: E402

st.set_page_config(page_title="Data & Methods", layout="wide")
st.title("Data and Methodology")

st.markdown(
    r"""
### Data sources

| Region | Input | Period | Elevation span |
|--------|--------|--------|----------------|
| **Caucasus** | Cleaned monthly CSVs (`tmean_c_month`, Tmax/Tmin) | **1959–1992** common window | 118 m (Zugdidi) – 2854 m (Mamisoni Pass) |
| **SENAMHI Peru** | Daily clean CSVs → aggregated monthly/annual | **1967–1992** & **2004–2019** | Coastal to high Andes |
| **Lascar EDW** | Hourly loggers → monthly means | **2006–2025** | ~3955–4760 m transect |

### Cleaning and completeness

**Caucasus:** Station-specific parsers produce `derived/*_monthly_clean.csv`. Completeness audit classifies each
station-month (valid vs missing vs NaN temperature). Annual analysis requires **≥ 10 valid months** per station-year.

**SENAMHI:** Raw semicolon CSVs; sentinel **−9999** → NaN; daily `tmean_c` from (Tmax+Tmin)/2.  
- **Month valid:** ≥ **24** days with finite `tmean_c`  
- **Year valid:** ≥ **10** valid months  
Availability heatmaps: `Senamhi_Weather_Stations/missing_months/`.

**Lascar:** ≥ **24** days per month; duplicate site excluded upstream.
"""
)

st.subheader("Regression model (shared)")

st.latex(r"z = m \cdot T + b")
st.markdown(
    """
- **z:** station elevation (m a.s.l.)  
- **T:** station mean temperature (°C) — annual or seasonal mean  
- **Lapse rate:** LR = **−1000 / m** (°C/km)  
- **Freezing level:** **FL = b** (elevation where fitted T = 0 °C)

**Limitation:** This is a **spatial** fit across a mountain network, **not** a vertical atmospheric profile.
Leverage, station density, and local inversions affect slopes; interpret trends as **descriptive** unless
supported by independent tests (not claimed here).
"""
)

st.subheader("Seasonal lapse rate (Option A)")

st.markdown(
    r"""
For each calendar year, rank months 1–12 by **regional mean** `tmean_c_month` across stations.  
**Warm season** = 4 highest months; **cool season** = 4 lowest (disjoint sets).  
Warm and cool regressions use the **same station set** (intersection with complete seasonal means).

| Quality rule | Caucasus | SENAMHI (typical relaxed runs) |
|--------------|----------|--------------------------------|
| Station fraction | ≥ **75%** of network in warm∩cool | **50%** (historical) or **67%** (modern) |
| Months per season | **4 of 4** required | **3 of 4** in relaxed Peru runs |
| Elevation check | Abs(Δ min elevation) < 200 m | Same (0 m when same stations) |
"""
)

st.subheader("Caucasus completeness summary (1959–1992)")

summary = load_caucasus_completeness_summary()
if summary.empty:
    exp = caucasus_completeness_summary_path()
    st.warning(f"Completeness summary CSV not found at:\n`{exp}`")
else:
    st.dataframe(summary, use_container_width=True, hide_index=True)

heatmap_dir = CAUCASUS / "completeness_audit" / "monthly_grids_1959-1992_(missing_data)"
pngs = sorted(heatmap_dir.glob("*_1959_1992.png")) if heatmap_dir.is_dir() else []
if pngs:
    station = st.selectbox("Station monthly availability heatmap", [p.stem for p in pngs])
    chosen = next(p for p in pngs if p.stem == station)
    st.image(str(chosen), caption=station.replace("_", " "), use_container_width=True)
