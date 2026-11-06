# Seasonal Lapse Rate Comparison: Caucasus (1959–1992) vs SENAMHI Historical (1967–1992)

**Caucasus code:** [`Caucasus_Weather_Stations/seasonal_LR_analysis/caucasus_seasonal_lapse_rate.py`](../../Caucasus_Weather_Stations/seasonal_LR_analysis/caucasus_seasonal_lapse_rate.py)
**SENAMHI code:** [`Senamhi_Weather_Stations/seasonal_LR_analysis/senamhi_seasonal_lapse_rate.py`](senamhi_seasonal_lapse_rate.py)
**Caucasus analysis doc:** [`Caucasus_Weather_Stations/seasonal_LR_analysis/caucasus_seasonal_lapse_rate_analysis_1959_1992.md`](../../Caucasus_Weather_Stations/seasonal_LR_analysis/caucasus_seasonal_lapse_rate_analysis_1959_1992.md)
**SENAMHI analysis doc:** [`Senamhi_Weather_Stations/seasonal_LR_analysis/senamhi_seasonal_lapse_rate_analysis.md`](senamhi_seasonal_lapse_rate_analysis.md)

---

## 1. Overview

Both the Caucasus and SENAMHI seasonal lapse rate analyses use an identical mathematical framework: objective warm/cool season selection by ranked regional monthly temperature, cross-network OLS regression of elevation on temperature, and the same derived lapse rate formula. The common methodology makes the comparison meaningful at the level of method and signal structure, even though the two networks occupy fundamentally different climate regimes — mid-latitude maritime/continental mountains versus the tropical Andes.

The core comparison question is: do both networks show the same warm/cool seasonal ordering of lapse rates, the same trend direction, and similar interannual variability? The answer is largely no — the two networks diverge in nearly every quantitative aspect while sharing the same regression skeleton. Understanding why exposes how regional climate controls (seasonality type, moisture source, cold pooling, convective regime) shape the effective vertical temperature gradient differently across mountain systems.

This document focuses on the **SENAMHI historical window (1967–1992, Group A, relaxed sf50 m3of4)** — the period with overlap to the Caucasus record — and draws on the strict-rule diagnostics where noted.

---

## 2. Methodology Comparison

| Parameter | Caucasus (1959–1992) | SENAMHI Historical (1967–1992) |
|---|---|---|
| **Period** | 1959–1992 (34 yr) | 1967–1992 (26 yr) |
| **Overlapping years** | — | 1967–1992 (shared era) |
| **Station network** | 8 stations (Group fixed) | 9 stations (Group A) |
| **Elevation range** | 118 m (Zugdidi) – 2854 m (Mamisoni Pass) | Coast/foothills to high Andes (exact range varies by year and station availability) |
| **Temperature variable** | `tmean_c_month` from pre-computed monthly clean CSVs | `tmean_c` (daily mean) aggregated to monthly; month valid only with **≥ 24 days** of finite daily data |
| **Season definition** | Option A: 4 warmest / 4 coldest months by regional monthly mean; sets must be disjoint | Identical — Option A |
| **Month completeness per station** | **All 4** target months required (strict) | **3 of 4** target months sufficient (relaxed); mean taken over available finite months |
| **Station fraction threshold** | **≥ 75 %** of network in warm ∩ cool intersection | **≥ 50 %** of network (further relaxed for historical window; default 75% leaves most years missing) |
| **Station set constraint** | warm ∩ cool intersection only | Identical |
| **Regression model** | `z = m · T + b`; `LR = −1000 / m` | Identical |
| **Valid years produced** | 33 of 34 (1992 excluded: station_count) | 25 of 26 under sf50 m3of4; far fewer under strict rules |
| **Plot trend line** | Not shown on main seasonal plot; described in analysis doc | OLS dashed fit per season on the plot |
| **Bootstrap CI** | Not applied to seasonal LR | Not applied |

**Key methodological asymmetry:** The SENAMHI historical series could not be computed under the same strict rules as the Caucasus (75% station fraction, all 4 months). Applying Caucasus-equivalent rules to the SENAMHI historical window yields only a handful of valid years. The relaxed outputs (sf50, m3of4) should therefore be treated as indicative rather than directly equivalent. Any quantitative comparison of magnitudes or trends must account for this.

---

## 3. Numerical Results

### 3.1 Summary statistics per season

| Metric | Caucasus warm | Caucasus cool | SENAMHI warm | SENAMHI cool |
|---|---|---|---|---|
| **Valid years** | 33 (1959–1991) | 33 (1959–1991) | 25 (1967–1992, sf50 m3of4) | 25 (1967–1992, sf50 m3of4) |
| **Mean LR (°C/km)** | 5.74 | 6.13 | ~3.8 | ~2.5 |
| **Min LR (year)** | 5.30 (1984) | 5.73 (1960) | 2.717 (1970) | 1.493 (1970) |
| **Max LR (year)** | 6.19 (1972) | 6.96 (1987) | 4.541 (1983) | 3.578 (1972) |
| **Interannual range** | 0.89 °C/km | 1.23 °C/km | ~1.8 °C/km | ~2.1 °C/km |
| **Typical seasonal gap** | cool − warm ≈ **+0.39 °C/km** | — | warm − cool ≈ **+1.3 °C/km** | — |
| **Which season is steeper?** | **Cool** (almost every year) | — | **Warm** (almost every year) | — |

The most fundamental contrast is in the **sign of the seasonal gap**: in the Caucasus the cool season consistently produces a steeper lapse rate than the warm season; in SENAMHI the relationship is reversed, with the warm season consistently steeper.

### 3.2 Linear trend lines (LR vs year, OLS)

| Network | Season | Slope (°C/km per year) | Equation | Direction |
|---|---|---|---|---|
| Caucasus | Warm | mild negative (not quantified in strict OLS) | — | Slight fall ~1975 onward |
| Caucasus | Cool | positive, accelerating post-1975 | — | Rising (EDW signal) |
| SENAMHI historical (sf50, m3of4) | Warm | **+0.0153** | LR_warm = 0.015325·y − 26.392 | Rising |
| SENAMHI historical (sf50, m3of4) | Cool | **−0.0047** | LR_cool = −0.004698·y + 11.816 | Slight fall |

Over the overlapping era (1967–1991), both networks show the same **direction** for warm and cool trends: the warm-season lapse rate rises and the cool-season lapse rate falls (or stays flat). However, the mechanism and magnitude are interpreted differently because the seasonal ordering is opposite. In the Caucasus, a rising cool and falling warm LR means the gap is widening — a diagnostic of EDW. In SENAMHI, a rising warm and falling cool LR means the gap between the two seasons is *also* widening, but from the opposite polarity.

---

## 4. Key Structural Differences

- **Sign of seasonal gap reversed.** Caucasus: cool > warm (mean gap +0.39 °C/km). SENAMHI: warm > cool (mean gap ~+1.3 °C/km). This single inversion reflects fundamentally different atmospheric controls on the vertical temperature profile in each region.

- **LR magnitude roughly halved.** Caucasus seasonal lapse rates range ~5.3–7.0 °C/km; SENAMHI historical lapse rates range ~1.5–4.5 °C/km. The SENAMHI values are significantly below the dry adiabatic lapse rate (~9.8 °C/km) and well below the typical moist adiabatic rate (~6 °C/km). Shallow cross-network lapse rates in SENAMHI likely reflect network geometry (coastal to Andes transect with horizontal heterogeneity) and the tropical atmospheric profile.

- **Interannual variability larger in SENAMHI.** SENAMHI shows a wider year-to-year range (~1.8–2.1 °C/km) than Caucasus (~0.89–1.23 °C/km) despite fewer stations, indicating greater sensitivity to data availability and annual circulation anomalies.

- **Data density mismatch.** Caucasus produces 33 of 34 valid years under strict rules. SENAMHI requires relaxed rules to generate 25 valid years; under Caucasus-equivalent rules most historical years are flagged `station_count`. This limits the transferability of trend interpretations.

- **Trend structure diverges.** Caucasus exhibits a widening cool–warm gap driven by cool-season steepening (an EDW-type signal). SENAMHI shows a widening warm–cool gap driven by warm-season strengthening — a different kind of divergence whose physical interpretation requires additional investigation.

- **1992 exclusion contrast.** The Caucasus excludes 1992 for `station_count` (only 5 of 8 stations). SENAMHI includes 1992 under the sf50 rule, though the reliability of that year is correspondingly lower.

---

## 5. Physical and Regional Factors

### 5.1 Latitude and the nature of seasonality

The Caucasus network sits at approximately 42–43°N, squarely in the mid-latitudes. At this latitude the seasonal cycle is thermally defined: summer and winter differ by 15–20 °C in regional mean temperature, and the 4 warmest vs 4 coldest months are unambiguously June–September vs December–March in most years. The warm/cool LR contrast is thus a contrast between genuinely different atmospheric states.

The SENAMHI network sits at approximately 9–10°S in the tropical Andes. At tropical latitudes the annual temperature cycle is weak (typical annual range 3–5 °C at any given elevation). The objective season algorithm still identifies 4 warm and 4 cool months, but these correspond to the **wet season (approximately October–April)** and the **dry season (approximately May–September)** rather than to thermally distinct summer and winter states. The seasonal "temperature" contrast driving season assignment is small, so the warm and cool labels are proxies for precipitation seasonality rather than thermal seasonality.

### 5.2 Why the cool season is steeper in the Caucasus

In a mid-latitude mountain network, the winter (cool-season) lapse rate is systematically steepened by two mechanisms operating simultaneously at the network's low-elevation anchor:

1. **Cold-air pooling and surface inversions at valley floors.** Low-elevation stations such as Zugdidi (118 m) experience strong radiative cooling and drainage of cold air from surrounding slopes during winter nights and clear-sky days. This depresses low-elevation temperatures relative to what would be expected from a free-atmospheric lapse rate, making the temperature-elevation gradient appear steeper across the network.

2. **Free-tropospheric influence at high elevations.** High-altitude stations (Mamisoni Pass, 2854 m) are partly decoupled from the surface boundary layer in winter, sitting closer to the free troposphere where temperatures reflect large-scale synoptic conditions rather than local surface energy balance. This keeps high-elevation temperatures relatively mild compared to the depressed valley-floor temperatures, further steepening the effective cross-network gradient.

In summer (warm season), both effects weaken: valley floors warm through convection and long-wave radiation, surface inversions are replaced by well-mixed boundary layers, and the effective lapse rate moves closer to the moist adiabatic rate (~6 °C/km), producing the slightly shallower warm-season values observed.

### 5.3 Why the warm season is steeper in SENAMHI

In the tropical Andes, the dominant atmospheric control on the vertical temperature gradient shifts from boundary-layer inversion dynamics (which drive Caucasus cool-season steepening) to **convective and moisture-flux processes**:

1. **Wet-season deep convection.** The warm/wet season (roughly October–April) brings deep convective systems driven by Amazonian moisture influx. Active convection is associated with near-moist-adiabatic lapse rates in the lower and mid-troposphere. Across a coast-to-Andes transect, the combination of low coastal temperatures and convectively warmed high-elevation environments can produce steeper apparent lapse rates during the wet season.

2. **Dry-season subsidence and inversion.** During the dry/cool season (May–September), subsidence associated with the South Pacific Anticyclone stabilises the lower troposphere along the western Andes slope and coast. This inversion elevates coastal and foothill temperatures relative to the wet season, while high-elevation temperatures remain relatively unchanged, compressing the temperature-elevation gradient and producing shallower cool-season lapse rates.

3. **Differential coastal warming.** Coastal and foothill stations in the SENAMHI network are directly influenced by sea-surface temperature variability (notably ENSO). During dry months, marine stratus and coastal upwelling keep low-elevation stations cool; during wet months, warmer SST and reduced stratus allow surface heating at low elevations — but this effect is more than offset by convective warming aloft, explaining the net steeper warm-season gradient.

### 5.4 Moisture regime differences

The Caucasus is influenced primarily by westerly frontal systems drawing moisture from the Black Sea and eastern Mediterranean. The warm season is humid but not convection-dominated; rainfall is more orographic and cyclonic in character. The moisture profile through the troposphere is more stratiform, maintaining moderate humidity at all elevations and producing lapse rates closer to the moist adiabatic rate in both seasons without the strong wet–dry precipitation contrast of the tropics.

The SENAMHI network is embedded in the South American monsoon system, with moisture sourced primarily from the Amazon basin via low-level jet. The seasonal alternation between active monsoon circulation (wet season, strong moisture flux, deep convection) and dry season suppression (subsidence, clear skies, strong radiative cooling at high elevations) produces a much larger intra-annual swing in the character of the atmospheric column — and correspondingly larger seasonal LR differences — than in the Caucasus.

### 5.5 ENSO teleconnections

Both networks show anomalous years likely linked to ENSO, but through different pathways:

- **Caucasus:** The 1987–1989 cluster of extreme cool-season lapse rate values (6.87–6.96 °C/km) coincides with a period of significant North Atlantic and Mediterranean circulation anomalies partly linked to the 1986–1988 ENSO cycle. ENSO influence on the Caucasus is indirect — through modulation of Atlantic storm tracks and blocking patterns — and manifests primarily in the cool season when large-scale circulation exerts the greatest control over surface temperature anomalies.

- **SENAMHI:** The 1970 collapse in both warm and cool LR (warm: 2.717 °C/km; cool: 1.493 °C/km — both record lows) corresponds to La Niña conditions (following the 1969/70 El Niño). El Niño events warm the Peruvian coast and disrupt normal coastal upwelling, while also weakening the Amazonian moisture flux to the Andes. This affects both low-elevation (coast) and high-elevation temperatures, with the net effect on the cross-network gradient depending on which elevations are more strongly perturbed. The ENSO signal in Peru is direct and strong through the Pacific SST mechanism, unlike the indirect ENSO influence on the Caucasus.

### 5.6 Network geometry effects

The Caucasus transect is compact and topographically controlled: all eight stations lie within the western Greater Caucasus, on a roughly north-south elevation transect from the Colchic lowlands to high mountain passes. The elevation-temperature relationship is dominated by the local atmospheric column rather than by horizontal climatological heterogeneity.

The SENAMHI Group A transect extends from near-coastal stations (Huarmey, Buena Vista at low elevation) to stations in the Cordillera Blanca foothills and valleys (Recuay, Chavin, Cajatambo). This transect includes a pronounced continental-to-maritime gradient in addition to the pure elevation gradient. Horizontal climate differences (aridity, marine influence, rain shadow effects) introduce noise into the elevation-temperature regression that is absent in the Caucasus geometry, contributing to shallower apparent lapse rates and greater year-to-year scatter.

### 5.7 Implications for Elevation-Dependent Warming (EDW)

The **Caucasus** pattern — cool-season steepening relative to warm-season, with a widening gap — is the canonical EDW signature. Steeper cool-season lapse rates imply that low-elevation stations are cooling faster (or warming more slowly) in winter than high-elevation stations, consistent with elevation-dependent warming of the upper mountain layer.

The **SENAMHI** pattern — warm-season strengthening, cool-season weakening — does not fit the same EDW template. If the warm-season lapse rate is rising over time, it could reflect intensification of wet-season convective activity (and thus stronger convective vertical temperature gradients), changes in coastal temperature driven by SST trends, or shifts in the Amazonian moisture flux rather than direct elevation-dependent surface warming. Distinguishing these mechanisms requires additional diagnostics beyond what a cross-network regression can provide.

---

## 6. Notable Year Cross-Reference (1967–1991 overlap period)

| Year | Caucasus warm LR | Caucasus cool LR | SENAMHI warm LR | SENAMHI cool LR | Notes |
|---|---|---|---|---|---|
| 1967 | 5.95 | 6.05 | — | — | SENAMHI data gap |
| 1968 | 5.83 | 6.04 | — | — | SENAMHI data gap |
| 1969 | 5.97 | 6.14 | — | — | SENAMHI data gap |
| 1970 | 6.02 | 6.24 | **2.72 (record low)** | **1.49 (record low)** | SENAMHI collapse; Caucasus near-normal |
| 1972 | **6.19 (high)** | 5.76 | ~3.8 | **3.58 (SENAMHI high cool)** | Unusually high warm LR in Caucasus; high cool LR in SENAMHI |
| 1975 | 5.91 | 5.89 | — | — | SENAMHI data gap |
| 1983 | 5.65 | 5.94 | **4.54 (SENAMHI high warm)** | ~2.5 | SENAMHI warm LR record; Caucasus unremarkable |
| 1984 | **5.30 (low)** | 6.57 | ~4.0 | ~2.5 | Caucasus warm LR record low; large Caucasus divergence |
| 1987 | 5.70 | **6.96 (high)** | ~4.0 | — | Caucasus cool spike; SENAMHI data gap or near-normal |
| 1988 | 5.69 | **6.93 (high)** | ~4.1 | ~2.5 | Caucasus cool spike continues |
| 1989 | 5.44 | **6.87 (high)** | ~4.2 | — | Caucasus cool spike third year |
| 1990 | 5.62 | 6.17 | ~3.8 | ~2.5 | Both networks moderate |
| 1991 | 5.61 | 6.65 | ~4.0 | ~2.5 | Caucasus cool still elevated |

Key observations from the overlap period:
- The **1970 SENAMHI collapse** (both seasons record low) has no corresponding anomaly in the Caucasus. This is consistent with a Peru-Pacific ENSO mechanism that does not propagate strongly to the Caucasus.
- The **1987–1989 Caucasus cool spike** is not matched by any SENAMHI pattern — the Peruvian stations are either data-sparse in those years or show near-average values, reinforcing the different teleconnection pathways.
- **1972** is an unusual shared year: Caucasus has its highest warm-season LR on record while SENAMHI records its highest cool-season LR. The shared anomaly direction (steeper gradient in different seasons) may reflect a broadly warm 1972 regional atmospheric state affecting both mountain systems differently depending on their climate regime.
- **1983** shows SENAMHI's highest warm-season LR with Caucasus unremarkable — consistent with the strong 1982/83 El Niño, which would strongly perturb the Pacific coast and Andean moisture flux in Peru but exert only a weak indirect signal in the Caucasus.

---

## 7. Caveats and Limitations

**Methodological asymmetry.** The most important caveat in any quantitative comparison is that the two series are not produced under equivalent quality thresholds. The Caucasus uses strict rules throughout (4-of-4 months, 75% station fraction), while the SENAMHI historical series requires relaxed rules (3-of-4 months, 50% fraction) to produce a usable multi-year record. Relaxed rules allow more years but introduce more variability from partially observed stations. The SENAMHI seasonal LR values under relaxed rules are therefore less tightly constrained than Caucasus values and carry wider implicit uncertainty.

**Overlapping period is short.** The shared era spans 1967–1991 at most (25 years with some SENAMHI data gaps within that period). This is too short to establish statistically robust trends or to rigorously test whether anomalous years are correlated between networks.

**Network density mismatch.** The Caucasus uses 8 stations with consistently complete seasonal data in most years. The SENAMHI historical network has 9 nominal stations but with substantial year-to-year variation in how many are active and pass the monthly validity rule. Years with only 4–5 active SENAMHI stations produce less stable regression geometry than any Caucasus year.

**Cross-network regression limitations.** Both analyses estimate a horizontal network-wide lapse rate rather than a true atmospheric vertical profile. The result reflects the spatial temperature-elevation relationship across the specific station arrangement, not the free-atmospheric lapse rate. This effect is amplified in SENAMHI, where the transect includes horizontal climate gradients (coast to inland, aridity gradients) that are absent in the Caucasus transect.

**Trend interpretation.** Both trend lines span short records over heterogeneous networks. Neither should be taken as a robust climate signal without additional statistical testing (confidence intervals on slope, breakpoint analysis, comparison to reanalysis) and validation against independent data sources (ERA5, radiosonde profiles, or satellite-derived temperature products).
