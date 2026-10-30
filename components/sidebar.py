"""Shared sidebar helpers."""
from __future__ import annotations

import streamlit as st


def year_range_slider(
    label: str,
    y0: int,
    y1: int,
    key: str,
) -> tuple[int, int]:
    return st.sidebar.slider(label, min_value=y0, max_value=y1, value=(y0, y1), key=key)
