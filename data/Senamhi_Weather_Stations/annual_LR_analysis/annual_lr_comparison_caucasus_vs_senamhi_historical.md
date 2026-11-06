# Annual Lapse Rate Comparison: Caucasus (1959–1992) vs SENAMHI Historical (1967–1992)

**Caucasus code:** [`Caucasus_Weather_Stations/annual_LR_analysis/caucasus_annual_lapse_rate_timeseries.py`](../../Caucasus_Weather_Stations/annual_LR_analysis/caucasus_annual_lapse_rate_timeseries.py)
**SENAMHI code:** [`Senamhi_Weather_Stations/annual_LR_analysis/senamhi_annual_lapse_rate_timeseries.py`](senamhi_annual_lapse_rate_timeseries.py)
**Caucasus analysis doc:** [`Caucasus_Weather_Stations/annual_LR_analysis/caucasus_annual_lapse_rate_analysis_1959_1992.md`](../../Caucasus_Weather_Stations/annual_LR_analysis/caucasus_annual_lapse_rate_analysis_1959_1992.md)
**SENAMHI analysis doc:** [`Senamhi_Weather_Stations/annual_LR_analysis/senamhi_annual_lapse_rate_analysis.md`](senamhi_annual_lapse_rate_analysis.md)

---

## 1. Overview

Both the Caucasus and SENAMHI annual lapse rate analyses use identical regression methodology: for each year, each station's annual mean temperature is computed from valid monthly data, and ordinary least squares regression of elevation on temperature is fitted across the network. The derived lapse rate (LR = −1000 / m) and freezing level (FL = b) emerge from the same formula in both cases.

Despite the shared framework, the two networks produce results that differ in magnitude, trend direction, interannual variability, and the physical interpretability of derived quantities. These differences are rooted in contrasting climate regimes (mid-latitude vs tropical), station network geometry and density, and the atmospheric processes controlling the vertical temperature gradient in each region.

This comparison focuses on the **overlapping era (1967–1991)** where direct year-to-year cross-network comparison is possible, drawing on the full Caucasus record (1959–1992) and the SENAMHI historical window (1967–1992, Group A, 9 nominal stations).

---

## 2. Methodology Comparison

| Parameter | Caucasus (1959–1992) | SENAMHI Historical (1967–1992) |
|---|---|---|
| **Period** | 1959–1992 (34 yr) | 1967–1992 (26 yr) |
| **Overlapping years** | — | 1967–1991 (shared era) |
| **Station group** | 8 stations, fixed throughout | Group A — 9 nominal stations |
| **Elevation range** | 118 m (Zugdidi) – 2854 m (Mamisoni Pass) | Coast/foothill to high Andes; varies by year |
| **Temperature source** | `tmean_c_month` from pre-computed monthly clean CSVs | Daily `tmean_c` → monthly (≥ 24 valid days per month) → annual (≥ 10 valid months) |
| **Annual mean requirement** | ≥ 10 valid months per station | Same (≥ 10 valid months) |
| **Min stations for LR fit** | Implicitly all 8 (always met; drops to 6–7 in late years) | **≥ 3** explicit lower bound; 3–7 in practice |
| **Regression model** | `z = m · T + b`; `LR = −1000/m`; `FL = b` | Identical |
| **Low-R² flag threshold** | R² < 0.4 | Same |
| **2σ outlier flag** | Yes — relative to the 1959–1992 period mean | Yes — relative to the 1967–1992 period mean |
| **5-year rolling mean** | Computed and stored in CSV (not plotted) | Not computed |
| **Gap bridge** | Not needed (no missing years) | Linear interpolation through 1987 for display only |
| **Valid years produced** | **34 of 34** | **25 of 26** (1987 missing: only 2 qualifying stations) |

**Key methodological asymmetry:** SENAMHI's daily-to-monthly aggregation step (≥ 24 days per month) adds a filtering layer absent in the Caucasus pipeline, which receives pre-computed monthly means. This means SENAMHI monthly means may exclude months with substantial data gaps that would be retained in a pre-aggregated format. The practical effect is that SENAMHI station-years with moderate data quality drop out more readily, explaining the sparser per-year station counts.

---

## 3. Numerical Results

### 3.1 Climatology and spread

| Metric | Caucasus (1959–1992) | SENAMHI Historical (1967–1992) |
|---|---|---|
| **Valid years** | 34 | 25 |
| **Mean LR (°C/km)** | **5.83** | **3.22** |
| **σ (°C/km)** | 0.18 | 0.24 |
| **Coefficient of variation** | ~3.1 % | ~7.4 % |
| **Min LR (year)** | 5.217 (1986) | 2.755 (1973) |
| **Max LR (year)** | 6.136 (1992) | 3.842 (1976) |
| **LR range** | 0.92 °C/km | 1.09 °C/km |
| **2σ outlier years** | 1971 (low), 1986 (low) | 1976 (high) |
| **Missing years** | 0 | 1 (1987) |
| **Typical R²** | > 0.98 in all years | 0.73 – 1.00 (wide range) |
| **Typical n\_stations per year** | 8 (6–7 in 1983, 1986–1992) | 3–7 (sparse and variable) |

The Caucasus mean LR of 5.83 °C/km is approximately **1.8× larger** than the SENAMHI historical mean of 3.22 °C/km. Despite a lower absolute value, SENAMHI shows proportionally **2.4× greater interannual variability** (CV 7.4 % vs 3.1 %), reflecting the combined effect of a sparser network and greater sensitivity to ENSO-driven temperature perturbations.

### 3.2 Linear trend lines (LR vs year)

| Network | Slope (°C/km per year) | Equation | Direction |
|---|---|---|---|
| Caucasus (1959–1992) | **+0.0020** | LR_trend(y) ≈ 0.00203 · y + constant | Slight rise |
| SENAMHI historical (1967–1992) | **−0.0047** | LR(y) = −0.004662 · y + 12.447 | Slight fall |

The trend slopes are **opposite in sign**. The Caucasus lapse rate gently increased over 1959–1992 (total change ≈ +0.067 °C/km over 33 years), while SENAMHI's lapse rate gently declined over 1967–1992 (total change ≈ −0.122 °C/km over 26 years). Both slopes are small relative to interannual σ and should be interpreted with caution over these short records.

### 3.3 Freezing level comparison

| Network | FL range (m a.s.l.) | Physically meaningful? |
|---|---|---|
| Caucasus | 2245 – 2768 m | **Yes** — within station elevation range (118–2854 m); the 0 °C isotherm lies between observed stations |
| SENAMHI historical | 5842 – 7651 m | **No** — extreme extrapolation artifact |

The SENAMHI freezing level values are not physically interpretable. Because the SENAMHI network lies in a tropical climate, all Group A stations have positive annual mean temperatures; even the highest-elevation stations remain above 0 °C on an annual average. When the regression line `z = m · T + b` is extrapolated to T = 0 °C, the intercept falls thousands of metres above the highest station — above any Andean peak — producing FL values of 5800–7600 m. This is a mathematical artifact of fitting a shallow-sloped line to a dataset that does not bracket 0 °C.

In the Caucasus, Mamisoni Pass (2854 m) has an annual mean temperature of approximately −2 °C, so the dataset does straddle 0 °C. The FL intercept is interpolated within the observed data range and represents a genuine estimate of the 0 °C isotherm altitude. The Caucasus FL column is a usable geophysical product; the SENAMHI FL column is not.

---

## 4. Key Structural Differences

- **LR magnitude is ~45 % lower in SENAMHI.** The Caucasus cross-network gradient (5.8–6.1 °C/km) is well above the moist adiabatic lapse rate (~6 °C/km), driven primarily by the steepening effect of cold-season cold pooling at low-elevation stations. SENAMHI's 3.2 °C/km is well below the moist adiabatic rate, reflecting a compressed temperature-elevation relationship across a tropical network where high-elevation stations remain warm relative to their altitude.

- **Trend directions are opposite.** The Caucasus shows a very slight upward trend in annual LR over 1959–1992; SENAMHI shows a slight downward trend over 1967–1992. This divergence is discussed in Section 6.

- **Caucasus R² is consistently near-perfect; SENAMHI R² spans a wide range.** Caucasus spatial coherence (R² > 0.98 every year) reflects a stable, thermally well-ordered elevation transect with 8 stations. SENAMHI R² ranges from 0.73 to values approaching 1.00 — the near-perfect values occur in years with only 3 stations (any 3 points define a near-perfect regression regardless of physical coherence), while lower R² years indicate genuine spatial disorder in the temperature-elevation relationship.

- **Interannual variability is proportionally larger in SENAMHI.** Despite a lower mean LR, SENAMHI's σ of 0.237 °C/km yields a coefficient of variation of 7.4 %, compared to 3.1 % for the Caucasus. This reflects both the sparser network (larger sampling uncertainty per year) and greater sensitivity to year-to-year climate forcing in the tropical Andes.

- **The SENAMHI freezing level is an extrapolation artifact.** Unlike the Caucasus FL (which is interpolated within the station elevation range), the SENAMHI FL column carries no physical meaning because the tropical climate regime keeps all stations above 0 °C annually.

- **SENAMHI loses 1987 entirely.** With only 2 qualifying stations in 1987, no LR estimate is possible that year. The Caucasus has no missing years across its full 34-year record.

---

## 5. Notable Year Cross-Reference (1967–1991 overlap)

| Year | Caucasus LR (°C/km) | Caucasus flag | SENAMHI LR (°C/km) | SENAMHI flag | Notes |
|---|---|---|---|---|---|
| 1967 | 5.940 | — | 3.056 | — | Both near-average |
| 1968 | 5.893 | — | 3.004 | — | Both slightly below mean |
| 1969 | 5.813 | — | 3.233 | — | Both near-average |
| 1970 | 6.043 | — | 3.352 | — | Both above mean |
| 1971 | **5.309** | **2σ low** | 3.187 | — | Caucasus anomalously low; SENAMHI normal |
| 1972 | 5.905 | — | **3.541** | — | Both elevated; **shared high anomaly** |
| 1973 | 5.862 | — | **2.755** | — | Caucasus normal; SENAMHI record low |
| 1974 | 5.813 | — | 3.491 | — | Caucasus normal; SENAMHI above average |
| 1975 | 5.875 | — | 3.460 | — | Both slightly above mean |
| 1976 | 5.639 | — | **3.842** | **2σ high** | Caucasus near-normal; SENAMHI record high |
| 1977 | 5.825 | — | 3.524 | — | Both above mean |
| 1978 | 5.839 | — | 3.298 | — | Both near-average |
| 1979 | 5.926 | — | 2.981 | — | Caucasus elevated; SENAMHI below mean |
| 1980 | 5.734 | — | 3.368 | — | Both near-average |
| 1981 | 5.846 | — | 2.915 | — | Caucasus normal; SENAMHI below mean |
| 1982 | 5.757 | — | 3.192 | — | Both near mean |
| 1983 | 5.761 | — | 3.335 | — | Both near mean |
| 1984 | 5.923 | — | 2.977 | — | Caucasus elevated; SENAMHI below mean |
| 1985 | 5.776 | — | 3.002 | — | Both slightly below mean |
| 1986 | **5.217** | **2σ low** | 2.975 | — | **Shared below-normal LR** |
| 1987 | 6.091 | — | — | missing | Caucasus high; SENAMHI missing |
| 1988 | 6.090 | — | 3.229 | — | Caucasus high; SENAMHI near-mean |
| 1989 | 5.787 | — | 3.236 | — | Both near-average |
| 1990 | 5.940 | — | 3.066 | — | Both near-average |
| 1991 | 5.829 | — | 3.197 | — | Both near-average |

**Key observations:**

- **1971 (Caucasus-only anomaly):** The Caucasus LR drops to 5.31 °C/km, its 2σ low — a year when November replaced March in the cool-season set, producing an unusually steep seasonal structure. SENAMHI is entirely unremarkable at 3.19 °C/km. The anomaly is internal to the Caucasus network and has no cross-network counterpart.

- **1972 (shared elevated LR):** Both networks show above-average annual lapse rates — Caucasus 5.91 °C/km (near its decadal high) and SENAMHI 3.54 °C/km (second-highest on record). A broadly warm regional state in 1972, following the 1971/72 La Niña, may have affected both mountain systems differently but in the same direction.

- **1973 (SENAMHI record low, Caucasus normal):** SENAMHI's 2.76 °C/km record low occurs with no Caucasus anomaly (5.86 °C/km). The 1972/73 La Niña brought anomalous cooling to parts of the tropical Andes while the Caucasus remained within its normal range.

- **1976 (SENAMHI record high, Caucasus normal):** SENAMHI's 2σ high (3.84 °C/km) falls in the year of the well-documented Pacific Decadal Oscillation phase transition. This PDO shift reorganised tropical Pacific SSTs and associated atmospheric circulation, producing a warm anomaly in the Peruvian Andes. No corresponding Caucasus anomaly is observed (5.64 °C/km, below average).

- **1986 (shared below-normal LR):** Both networks show below-average lapse rates in the same year — the Caucasus reaches its 2σ low (5.22 °C/km) and SENAMHI is below its mean (2.97 °C/km). This is the only year where both networks simultaneously flag an anomalously low cross-network gradient, suggesting a large-scale atmospheric circulation anomaly during the 1986/87 El Niño onset that affected both regions.

---

## 6. Physical and Regional Factors

### 6.1 LR magnitude gap (~2.6 °C/km)

The ~1.8× magnitude difference between the Caucasus (~5.83 °C/km) and SENAMHI (~3.22 °C/km) annual lapse rates reflects two reinforcing mechanisms:

**Cold-season cold pooling in the Caucasus.** At mid-latitudes (~43°N), the Caucasus network experiences a strong winter season during which the lowest-elevation station (Zugdidi, 118 m) is subject to radiative cooling, cold-air drainage from surrounding slopes, and surface temperature inversions. These effects depress annual-mean temperatures at the network's low-elevation anchor well below what would be expected from a free-atmospheric lapse rate. High-elevation stations (Mamisoni Pass, 2854 m) are partly decoupled from the surface boundary layer and sit closer to the free troposphere, which keeps them relatively mild in winter. The combined effect steepens the annual-mean temperature-elevation gradient to well above the moist adiabatic rate.

**Compressed tropical temperature gradient in SENAMHI.** At ~9–10°S, the annual temperature cycle is dominated by precipitation seasonality rather than thermal contrast. Low-elevation SENAMHI stations in the Pacific coastal corridor experience onshore winds, marine stratus influence, and coastal upwelling that moderate their temperatures year-round. High-elevation Andean stations benefit from solar insolation and are warmer relative to their altitude than mid-latitude alpine stations of equivalent elevation. The result is a compressed temperature-elevation gradient: the temperature difference between the network's lowest and highest stations is smaller per unit elevation than in the Caucasus, producing a shallower apparent lapse rate.

### 6.2 Opposite trend directions

The Caucasus shows a very slight positive trend in annual LR (+0.002 °C/km/yr over 1959–1992), while SENAMHI shows a slight negative trend (−0.005 °C/km/yr over 1967–1992). Although both slopes are small relative to interannual variability, their opposing directions are physically interpretable.

**Caucasus slight rise (consistent with seasonal analysis):** The companion seasonal lapse rate analysis shows that the Caucasus cool-season lapse rate was steepening progressively after ~1975, while the warm-season rate was weakly declining. The annual mean is a blend of both, and the net result is a slight positive trend — meaning the temperature-elevation gradient across the network was, on balance, becoming fractionally steeper over the record. This is consistent with low-elevation valley stations warming relatively less than expected, or high-elevation stations warming slightly more, on an annual basis.

**SENAMHI slight fall:** A declining annual LR in SENAMHI over 1967–1992 implies the temperature contrast between the network's low-elevation and high-elevation stations was gradually narrowing. One plausible driver is the preferential warming of Pacific coastal and foothill stations from rising eastern Pacific SSTs over the same period. If low-elevation stations warmed faster than high-elevation Andean stations — as might occur when the Pacific warming signal propagates onshore more efficiently than it reaches the Andean interior — the temperature-elevation slope would flatten, reducing the apparent lapse rate. This interpretation is speculative given the sparse station coverage and should be tested with reanalysis or radiosonde data.

### 6.3 R² instability in SENAMHI

The Caucasus produces spatially coherent regression fits (R² > 0.98) every year because 8 stations span a thermally well-ordered transect with consistent elevation-temperature ranking. In any year with 8 stations forming a monotonically ordered temperature-elevation sequence, R² is necessarily high.

SENAMHI's R² ranges from 0.73 to values approaching 1.00, driven primarily by the variable station count. In years with only 3 stations, R² approaches 1.00 by mathematical necessity — any 3 points lie near a line regardless of whether the relationship is physically coherent or a sampling artifact. R² values in the 0.73–0.85 range (occurring in 1978–1980 and 1985–1986) indicate years where the temperature-elevation relationship is genuinely noisy or where atypical spatial patterns (e.g. an anomalously warm high-elevation station or a cool coastal station) disrupt the expected ordering.

The practical implication is that high R² in SENAMHI should not be read as evidence of a robust lapse rate estimate when n_stations is 3 or 4. Years with 5–7 stations and R² > 0.87 (e.g. 1969, 1970, 1972, 1975, 1976) are the most reliable SENAMHI annual LR estimates in the historical window.

### 6.4 Freezing level contrast

The Caucasus FL (2245–2768 m) is geophysically meaningful because Mamisoni Pass (2854 m) has a negative annual mean temperature (~−2 °C), meaning the network brackets the 0 °C isotherm. Interpolating the regression to T = 0 °C yields a result within the station elevation range, cross-checkable against independent glaciological or snowline data for the region.

The SENAMHI FL (5842–7651 m) is a mathematical extrapolation with no climatological basis. All Group A stations have positive annual mean temperatures, so the regression line must be extended ~4000 m beyond the highest station to reach T = 0 °C. At such extreme extrapolation distances, the intercept is dominated by small errors in the regression slope and is not a useful proxy for any real atmospheric isotherm. For the tropical Andes, the actual 0 °C isotherm (freezing level) typically sits near 4800–5200 m — well below these extrapolated values and not recoverable from a cross-network regression where no station is cold enough to constrain it.

---

## 7. Caveats and Limitations

**Methodological asymmetry in temperature aggregation.** The Caucasus pipeline uses pre-computed monthly means (`tmean_c_month`) without an explicit daily data-density filter at the monthly level. SENAMHI filters monthly means through a ≥ 24-day daily coverage gate before annual aggregation. This additional filter means that months with moderate data quality (e.g. 20 valid days) are discarded from SENAMHI but would be retained in an equivalent Caucasus-format pipeline. This contributes to SENAMHI's lower per-year station counts and makes a strictly equivalent comparison difficult.

**Minimum stations threshold.** The Caucasus script does not enforce an explicit minimum station count (all 8 are available in most years). SENAMHI requires ≥ 3 stations per year, which is a much lower bar and admits years with minimal geometric constraint on the regression. Years with 3 SENAMHI stations are structurally underdetermined relative to any Caucasus year.

**Short and non-overlapping periods.** The Caucasus record begins 8 years before SENAMHI (1959 vs 1967). The shared era covers 1967–1991 at most — 25 years, with 24 pairs of comparable annual LR values (1987 missing in SENAMHI). This is insufficient for robust trend comparison or significance testing of the opposing slope signs.

**SENAMHI freezing level.** As described in Section 3.3, the SENAMHI FL column should not be used for geophysical interpretation. Any analysis drawing on FL from both datasets should use the Caucasus FL and acknowledge that no equivalent SENAMHI FL is available from this regression approach.

**Trend causality.** Both trend lines are purely descriptive OLS fits to short, heterogeneous station networks. Neither can be attributed to a specific climate mechanism without additional evidence from reanalysis products, radiosondes, or satellite-derived temperature profiles that are independent of the surface station network.
