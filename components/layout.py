"""Streamlit layout helpers (API compatibility)."""
from __future__ import annotations

# Streamlit 1.47+ deprecates use_container_width in favor of width=
try:
    import streamlit as st

    _v = getattr(st, "__version__", "0")
    _major, _minor = (int(x) for x in _v.split(".")[:2])
    USE_WIDTH_STRETCH = _major > 1 or (_major == 1 and _minor >= 47)
except Exception:
    USE_WIDTH_STRETCH = False

# Plotly charts: prefer stretch when available
PLOTLY_KW = {"width": "stretch"} if USE_WIDTH_STRETCH else {"use_container_width": True}
# st.dataframe / images
DF_KW = {"width": "stretch"} if USE_WIDTH_STRETCH else {"use_container_width": True}
IMG_KW = {"width": "stretch"} if USE_WIDTH_STRETCH else {"use_container_width": True}


def plotly_kwargs() -> dict:
    return dict(PLOTLY_KW)


def df_kwargs() -> dict:
    return dict(DF_KW)


def img_kwargs() -> dict:
    return dict(IMG_KW)
