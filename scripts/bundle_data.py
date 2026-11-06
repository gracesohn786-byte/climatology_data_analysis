"""
Copy derived CSVs into streamlit_app/data/ for Streamlit Cloud (app-only repos).

Run from repository root (parent of streamlit_app/) or from streamlit_app/:

  python streamlit_app/scripts/bundle_data.py

Commit the resulting streamlit_app/data/ folder so Cloud deployments can load CSVs.
"""
from __future__ import annotations

import shutil
from pathlib import Path


def main() -> None:
    script = Path(__file__).resolve()
    streamlit_app = script.parent.parent
    repo_root = streamlit_app.parent
    bundle = streamlit_app / "data"

    copies: list[tuple[Path, Path]] = []

    # Caucasus derived
    cauc_src = repo_root / "Caucasus_Weather_Stations" / "derived"
    cauc_dst = bundle / "Caucasus_Weather_Stations" / "derived"
    for name in [
        "caucasus_annual_lapse_rate_timeseries_1959_1992.csv",
        "caucasus_seasonal_lapse_rate_long_1959_1992.csv",
        "caucasus_seasonal_lapse_rate_diagnostics_1959_1992.csv",
        "caucasus_freezing_level_timeseries_1959_1992.csv",
        "caucasus_station_annual_climatology_1959_1992.csv",
        "station_metadata.csv",
    ]:
        copies.append((cauc_src / name, cauc_dst / name))
    copies.append(
        (
            cauc_src / "completeness_audit_1959_1992" / "caucasus_station_completeness_summary_1959_1992.csv",
            cauc_dst / "completeness_audit_1959_1992" / "caucasus_station_completeness_summary_1959_1992.csv",
        )
    )

    # SENAMHI derived
    sen_src = repo_root / "Senamhi_Weather_Stations" / "derived"
    sen_dst = bundle / "Senamhi_Weather_Stations" / "derived"
    for name in [
        "senamhi_annual_lapse_rate_1967_1992.csv",
        "senamhi_annual_lapse_rate_2004_2019.csv",
        "senamhi_seasonal_lapse_rate_long_1967_1992_relaxed_sf50_m3of4.csv",
        "senamhi_seasonal_lapse_rate_long_2004_2019_relaxed_sf67_m3of4.csv",
        "senamhi_seasonal_lapse_rate_long_1967_1992.csv",
        "senamhi_seasonal_lapse_rate_long_2004_2019.csv",
        "senamhi_freezing_level_timeseries_1967_1992_sf33.csv",
        "senamhi_freezing_level_timeseries_1967_1992_sf50.csv",
        "senamhi_freezing_level_timeseries_2004_2019_sf67.csv",
    ]:
        copies.append((sen_src / name, sen_dst / name))

    sen_fl = repo_root / "Senamhi_Weather_Stations" / "FL_timeseries_v2"
    sen_fl_dst = bundle / "Senamhi_Weather_Stations" / "FL_timeseries_v2"
    copies.append(
        (
            sen_fl / "senamhi_freezing_level_timeseries_v2_fixedpair_cajatambo_chavin_1994_2019.csv",
            sen_fl_dst / "senamhi_freezing_level_timeseries_v2_fixedpair_cajatambo_chavin_1994_2019.csv",
        )
    )

    # Lascar
    las_src = repo_root / "Peru_Lascar_EDW_temperature_humidity" / "seasonal_lr_analysis"
    las_dst = bundle / "Peru_Lascar_EDW_temperature_humidity" / "seasonal_lr_analysis"
    for name in [
        "lascar_seasonal_lr_timeseries_2006_2025.csv",
        "lascar_seasonal_lr_timeseries_relaxed_2006_2025.csv",
    ]:
        copies.append((las_src / name, las_dst / name))

    # --- Reference PNGs: copy into canonical paths under bundle (matches components.paths fallbacks) ---
    cauc_root = repo_root / "Caucasus_Weather_Stations"
    cauc_b = bundle / "Caucasus_Weather_Stations"

    def _bundle_png(dst_under_bundle: str, *src_candidates: Path) -> None:
        dst = bundle.joinpath(*Path(dst_under_bundle).parts)
        for s in src_candidates:
            if s.is_file():
                copies.append((s, dst))
                return

    _bundle_png(
        "Caucasus_Weather_Stations/annual_LR_analysis/caucasus_annual_lapse_rate_timeseries_1959_1992.png",
        cauc_root / "annual_LR_analysis" / "caucasus_annual_lapse_rate_timeseries_1959_1992.png",
        cauc_root / "derived" / "plots" / "lapse_rate" / "caucasus_annual_lapse_rate_timeseries_1959_1992.png",
    )
    _bundle_png(
        "Caucasus_Weather_Stations/seasonal_LR_analysis/caucasus_seasonal_lapse_rate_timeseries_1959_1992.png",
        cauc_root / "seasonal_LR_analysis" / "caucasus_seasonal_lapse_rate_timeseries_1959_1992.png",
        cauc_root / "derived" / "plots" / "lapse_rate" / "caucasus_seasonal_lapse_rate_timeseries_1959_1992.png",
    )
    _bundle_png(
        "Caucasus_Weather_Stations/seasonal_LR_analysis/caucasus_seasonal_lapse_rate_timeseries_1959_1992_old.png",
        cauc_root / "seasonal_LR_analysis" / "caucasus_seasonal_lapse_rate_timeseries_1959_1992_old.png",
    )
    _bundle_png(
        "Caucasus_Weather_Stations/FL_timeseries_analysis/caucasus_freezing_level_timeseries_1959_1992.png",
        cauc_root / "FL_timeseries_analysis" / "caucasus_freezing_level_timeseries_1959_1992.png",
        cauc_root / "derived" / "plots" / "lapse_rate" / "caucasus_freezing_level_timeseries_1959_1992.png",
    )
    _bundle_png(
        "Caucasus_Weather_Stations/LR_Elevation_vs_Temp_Analysis/plot/"
        "caucasus_lapse_rate_climatology_elevation_vs_temp_1959_1992.png",
        cauc_root
        / "LR_Elevation_vs_Temp_Analysis"
        / "plot"
        / "caucasus_lapse_rate_climatology_elevation_vs_temp_1959_1992.png",
    )

    sen_root = repo_root / "Senamhi_Weather_Stations"

    def _sen_bundle(rel: str, *srcs: Path) -> None:
        _bundle_png(f"Senamhi_Weather_Stations/{rel}", *srcs)

    _sen_bundle(
        "annual_LR_analysis/senamhi_annual_lapse_rate_1967_1992.png",
        sen_root / "annual_LR_analysis" / "senamhi_annual_lapse_rate_1967_1992.png",
        sen_root / "annual_lr_v3" / "senamhi_annual_lapse_rate_fixed_trio_1967_1992.png",
        sen_root / "annual_lr_v3" / "senamhi_annual_lapse_rate_fixed_pair_relaxed_m7_1967_1992.png",
        sen_root / "annual_LR_v2" / "senamhi_annual_lapse_rate_fixed_pair_1967_1992.png",
    )
    _sen_bundle(
        "annual_LR_analysis/senamhi_annual_lapse_rate_2004_2019.png",
        sen_root / "annual_LR_analysis" / "senamhi_annual_lapse_rate_2004_2019.png",
        sen_root / "annual_lr_v3" / "senamhi_annual_lapse_rate_fixed_trio_2004_2019.png",
        sen_root / "annual_lr_v3" / "senamhi_annual_lapse_rate_fixed_pair_relaxed_m7_2004_2019.png",
        sen_root / "annual_LR_v2" / "senamhi_annual_lapse_rate_fixed_pair_2004_2019.png",
    )
    _sen_bundle(
        "seasonal_LR_analysis/senamhi_seasonal_lapse_rate_timeseries_1967_1992_relaxed_sf50_m3of4.png",
        sen_root / "seasonal_LR_analysis" / "senamhi_seasonal_lapse_rate_timeseries_1967_1992_relaxed_sf50_m3of4.png",
        sen_root / "seasonal_LR_analysis" / "senamhi_seasonal_lapse_rate_timeseries_1967_1992_relaxed_sf67_m3of4.png",
        sen_root / "seasonal_LR_analysis" / "senamhi_seasonal_lapse_rate_timeseries_1967_1992.png",
        sen_root / "seasonal_lr_v2" / "senamhi_seasonal_lapse_rate_timeseries_1967_1992_fixed_pair_bv_aija_hist_relaxed_m2of4.png",
    )
    _sen_bundle(
        "seasonal_LR_analysis/senamhi_seasonal_lapse_rate_timeseries_2004_2019_relaxed_sf67_m3of4.png",
        sen_root / "seasonal_LR_analysis" / "senamhi_seasonal_lapse_rate_timeseries_2004_2019_relaxed_sf67_m3of4.png",
        sen_root / "seasonal_LR_analysis" / "senamhi_seasonal_lapse_rate_timeseries_2004_2019.png",
        sen_root / "seasonal_lr_v2" / "senamhi_seasonal_lapse_rate_timeseries_2004_2019_fixed_pair_bv_recuay_m3of4.png",
    )
    for fl_name in [
        "senamhi_freezing_level_timeseries_1967_1992_sf33.png",
        "senamhi_freezing_level_timeseries_1967_1992_sf50.png",
        "senamhi_freezing_level_timeseries_2004_2019_sf67.png",
        "freezing_level_trend_comparison_caucasus_vs_senamhi.png",
    ]:
        _sen_bundle(f"FL_timeseries_analysis/{fl_name}", sen_root / "FL_timeseries_analysis" / fl_name)
    _sen_bundle(
        "FL_timeseries_v2/senamhi_freezing_level_timeseries_v2_fixedpair_cajatambo_chavin_1994_2019.png",
        sen_root / "FL_timeseries_v2" / "senamhi_freezing_level_timeseries_v2_fixedpair_cajatambo_chavin_1994_2019.png",
    )

    for las_png in [
        "lascar_seasonal_lr_timeseries_2006_2025.png",
        "lascar_seasonal_lr_timeseries_relaxed_2006_2025.png",
        "completeness_heatmap_llanup1.png",
        "completeness_heatmap_llanup2.png",
        "completeness_heatmap_llanup3.png",
        "completeness_heatmap_llanup4.png",
        "completeness_heatmap_llanport.png",
    ]:
        _bundle_png(
            f"Peru_Lascar_EDW_temperature_humidity/seasonal_lr_analysis/{las_png}",
            las_src / las_png,
        )

    # Comparison write-ups (Regional Comparison expander)
    for md_rel in [
        "annual_LR_analysis/annual_lr_comparison_caucasus_vs_senamhi_historical.md",
        "seasonal_LR_analysis/seasonal_lr_comparison_caucasus_vs_senamhi_historical.md",
    ]:
        _sen_bundle(md_rel, sen_root.joinpath(*Path(md_rel).parts))

    def _rel(p: Path) -> str:
        try:
            return str(p.relative_to(repo_root))
        except ValueError:
            return str(p)

    n_ok = 0
    for src, dst in copies:
        if not src.is_file():
            print(f"SKIP (missing): {_rel(src)}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print("OK", dst.relative_to(streamlit_app))
        n_ok += 1

    # Slim station map for Peru (avoids committing large daily_clean CSVs)
    map_csv = sen_dst / "senamhi_stations_map.csv"
    if sen_src.is_dir():
        rows = []
        import pandas as pd

        for p in sorted(sen_src.glob("*_daily_clean.csv")):
            try:
                head = pd.read_csv(p, nrows=1)
            except Exception:
                continue
            if {"latitude", "longitude", "elevation_m", "station_name"}.issubset(head.columns):
                rows.append(
                    {
                        "station_name": head["station_name"].iloc[0],
                        "latitude": head["latitude"].iloc[0],
                        "longitude": head["longitude"].iloc[0],
                        "elevation_m": head["elevation_m"].iloc[0],
                    }
                )
        if rows:
            map_csv.parent.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(rows).to_csv(map_csv, index=False)
            print("OK", map_csv.relative_to(streamlit_app))

    print(f"\nCopied {n_ok} files into {bundle}. Commit streamlit_app/data for Cloud.")


if __name__ == "__main__":
    main()
