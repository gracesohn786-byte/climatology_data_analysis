"""Plotly charts aligned with research figure styling."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

WARM_COLOR = "#d62728"
COOL_COLOR = "#1f77b4"
NEUTRAL_LINE = "#333333"
TREND_DASH = "dot"


def _empty_fig(title: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(title=title, template="plotly_white", height=420)
    fig.add_annotation(text="No data available", showarrow=False, y=0.5, x=0.5)
    return fig


def fig_annual_lr(df: pd.DataFrame, year_min: int, year_max: int, show_trend: bool = True) -> go.Figure:
    if df.empty or "year" not in df.columns:
        return _empty_fig("Annual lapse rate")
    sub = df[(df["year"] >= year_min) & (df["year"] <= year_max)].copy()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=sub["year"],
            y=sub["lapse_rate"],
            mode="lines+markers",
            name="Annual LR",
            line=dict(color=NEUTRAL_LINE, width=2),
        )
    )
    if show_trend and "lapse_rate_trend" in sub.columns:
        fig.add_trace(
            go.Scatter(
                x=sub["year"],
                y=sub["lapse_rate_trend"],
                mode="lines",
                name="Linear trend (OLS)",
                line=dict(color=NEUTRAL_LINE, dash=TREND_DASH),
            )
        )
    if "outlier_2sigma" in sub.columns:
        outs = sub[sub["outlier_2sigma"] == True]  # noqa: E712
        if not outs.empty:
            fig.add_trace(
                go.Scatter(
                    x=outs["year"],
                    y=outs["lapse_rate"],
                    mode="markers",
                    name="2σ outlier",
                    marker=dict(size=12, symbol="x", color="#e67e22"),
                )
            )
    fig.update_layout(
        title="Annual lapse rate (°C/km)",
        xaxis_title="Year",
        yaxis_title="Lapse rate (°C/km)",
        template="plotly_white",
        height=440,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig


def fig_seasonal_lr(
    long_df: pd.DataFrame,
    year_min: int,
    year_max: int,
    ylim: tuple[float, float] | None = None,
    show_trend: bool = False,
) -> go.Figure:
    if long_df.empty:
        return _empty_fig("Seasonal lapse rate")
    sub = long_df[(long_df["year"] >= year_min) & (long_df["year"] <= year_max)]
    wide = sub.pivot_table(index="year", columns="season", values="lapse_rate", aggfunc="first")
    fig = go.Figure()
    if "warm" in wide.columns:
        fig.add_trace(
            go.Scatter(
                x=wide.index,
                y=wide["warm"],
                mode="lines+markers",
                name="Warm",
                line=dict(color=WARM_COLOR, width=2),
            )
        )
    if "cool" in wide.columns:
        fig.add_trace(
            go.Scatter(
                x=wide.index,
                y=wide["cool"],
                mode="lines+markers",
                name="Cool",
                line=dict(color=COOL_COLOR, width=2),
            )
        )
    if show_trend:
        for season, color in (("warm", WARM_COLOR), ("cool", COOL_COLOR)):
            if season not in wide.columns:
                continue
            yv = wide[season].dropna()
            if len(yv) >= 2:
                coef = np.polyfit(yv.index.astype(float), yv.values, 1)
                trend = coef[0] * yv.index.astype(float) + coef[1]
                fig.add_trace(
                    go.Scatter(
                        x=yv.index,
                        y=trend,
                        mode="lines",
                        name=f"{season.title()} trend",
                        line=dict(color=color, dash=TREND_DASH),
                        showlegend=True,
                    )
                )
    layout = dict(
        title="Seasonal lapse rate: warm vs cool (°C/km)",
        xaxis_title="Year",
        yaxis_title="Lapse rate (°C/km)",
        template="plotly_white",
        height=440,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    if ylim:
        layout["yaxis"] = dict(range=list(ylim))
    fig.update_layout(**layout)
    return fig


def fig_freezing_level(df: pd.DataFrame, year_min: int, year_max: int, show_ci: bool = True) -> go.Figure:
    if df.empty:
        return _empty_fig("Freezing level")
    sub = df[(df["year"] >= year_min) & (df["year"] <= year_max)].copy()
    fig = go.Figure()
    if show_ci and {"fl_ci_lo", "fl_ci_hi"}.issubset(sub.columns):
        fig.add_trace(
            go.Scatter(
                x=sub["year"],
                y=sub["fl_ci_hi"],
                mode="lines",
                line=dict(width=0),
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=sub["year"],
                y=sub["fl_ci_lo"],
                mode="lines",
                fill="tonexty",
                fillcolor="rgba(31, 119, 180, 0.2)",
                line=dict(width=0),
                name="95% bootstrap CI",
            )
        )
    fig.add_trace(
        go.Scatter(
            x=sub["year"],
            y=sub["freezing_level_m"],
            mode="lines+markers",
            name="Freezing level",
            line=dict(color=NEUTRAL_LINE, width=2),
        )
    )
    if "fl_trend" in sub.columns:
        fig.add_trace(
            go.Scatter(
                x=sub["year"],
                y=sub["fl_trend"],
                mode="lines",
                name="Linear trend (OLS)",
                line=dict(color=NEUTRAL_LINE, dash=TREND_DASH),
            )
        )
    fig.update_layout(
        title="Freezing level altitude (m a.s.l.)",
        xaxis_title="Year",
        yaxis_title="Elevation (m)",
        template="plotly_white",
        height=440,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig


def fig_climatology_scatter(clim: pd.DataFrame, temp_col: str, label: str) -> go.Figure:
    if clim.empty or temp_col not in clim.columns:
        return _empty_fig("Climatology")
    df = clim.sort_values("elevation_m")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df[temp_col],
            y=df["elevation_m"],
            mode="markers",
            marker=dict(size=10, color="#2c5282"),
            name=label,
            text=df["station_name"],
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Temperature: %{x:.2f} °C<br>"
                "Elevation: %{y:.0f} m<extra></extra>"
            ),
        )
    )
    x = df[temp_col].to_numpy(dtype=float)
    z = df["elevation_m"].to_numpy(dtype=float)
    mask = np.isfinite(x) & np.isfinite(z)
    if mask.sum() >= 2:
        m, b = np.polyfit(x[mask], z[mask], 1)
        xs = np.linspace(x[mask].min(), x[mask].max(), 50)
        fig.add_trace(
            go.Scatter(x=xs, y=m * xs + b, mode="lines", name="OLS fit", line=dict(dash="dash", color="#718096"))
        )
        if m != 0:
            lr = -1000.0 / m
            fig.update_layout(
                annotations=[
                    dict(
                        x=0.98,
                        y=0.98,
                        xref="paper",
                        yref="paper",
                        xanchor="right",
                        yanchor="top",
                        showarrow=False,
                        align="right",
                        text=f"LR ≈ {lr:.2f} °C/km<br>FL ≈ {b:.0f} m",
                        bgcolor="rgba(255,255,255,0.85)",
                    )
                ]
            )
    fig.update_layout(
        title=f"Climatology: elevation vs {label}",
        xaxis_title=f"Temperature (°C) — {label}",
        yaxis_title="Elevation (m a.s.l.)",
        template="plotly_white",
        height=480,
    )
    return fig


def fig_r2_timeseries(df: pd.DataFrame, year_min: int, year_max: int) -> go.Figure:
    if df.empty or "r2" not in df.columns:
        return _empty_fig("Regression R²")
    sub = df[(df["year"] >= year_min) & (df["year"] <= year_max)]
    fig = go.Figure(
        go.Scatter(x=sub["year"], y=sub["r2"], mode="lines+markers", line=dict(color="#553c9a"))
    )
    fig.add_hline(y=0.4, line_dash="dash", line_color="#a0aec0", annotation_text="R² = 0.4 flag")
    fig.update_layout(
        title="Spatial regression R² by year",
        xaxis_title="Year",
        yaxis_title="R²",
        template="plotly_white",
        height=320,
        yaxis=dict(range=[0, 1.05]),
    )
    return fig
