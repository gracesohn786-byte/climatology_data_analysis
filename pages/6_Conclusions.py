"""Conclusions, limitations, future work."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bootstrap import ensure_streamlit_path  # noqa: E402

APP_DIR = ensure_streamlit_path()

st.set_page_config(page_title="Conclusions", layout="wide")
st.title("Conclusions and Implications")

st.markdown(
    """
### Major findings — Caucasus (centerpiece)

1. **Stable spatial coherence:** Annual cross-station regressions yield **R² > 0.98** (1959–1992); lapse rate
   varies smoothly year-to-year (mean **~5.83 °C/km**, σ **~0.18 °C/km**).
2. **Seasonal EDW-style signal:** Cool-season LR **exceeds** warm-season LR on average; the **warm/cool gap widens**
   after ~1975, with late-1980s cool-season peaks (**1987–1989**).
3. **Freezing level:** Interannual range **~2245–2768 m**; descriptive trend **~−2.18 m/yr** over 34 years—small
   relative to σ (~120 m) and late-year CI width when station count drops.
4. **Climatology:** Daytime (Tmax proxy) steepest LR / highest FL; nighttime weakest—diurnal proxy matters.

### Peru (SENAMHI & Lascar)

- **Shallower LR** (~3.2–3.5 °C/km) under the same regression geometry; historical network **sparse**, modern window **dense**.
- **Seasonal warm/cool** framework applies; relaxed station/month rules needed for continuous historical series.
- **Network FL not physical** in tropical annual means; use Caucasus FL for glaciological 0 °C interpretation from this method.
- **Lascar transect** confirms cool-season LR slightly steeper than warm at high elevation (~6.0–6.3 °C/km means, strict run).

### Evidence consistent with EDW?

Seasonal **divergence** in the Caucasus (steepening cool-season LR vs stable/weakening warm-season LR) is **consistent with**
elevation-dependent thermal structure changes, but this project reports **correlational / descriptive** trends—not causal attribution.

### Limitations

- Eight (Caucasus) or fewer (Peru historical) stations; **not** a vertical profile.
- Short records and opposing descriptive LR trends between regions caution against over-interpretation.
- SENAMHI daily→monthly gates differ from Caucasus pre-aggregated monthly inputs.
- No formal significance testing on trends in the underlying analysis pipeline.

### Future directions

- Extend Peru modern window; fixed-station pairs for stable geometry.
- Combine with reanalysis or radiosonde profiles to validate network slopes.
- Link LR/FL diagnostics to glacier mass-balance and snowline observations in each region.
"""
)

st.success(
    "Thank you for reviewing this presentation. Source code and data remain in the parent repository; "
    "this app reads derived outputs only."
)
