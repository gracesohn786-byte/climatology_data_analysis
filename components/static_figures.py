"""Embed original research PNGs with captions."""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from components.layout import img_kwargs


def show_static(path: Path, caption: str) -> None:
    if not path.is_file():
        st.warning(f"Reference figure not found: `{path.name}`")
        return
    st.image(str(path), caption=caption, **img_kwargs())


def show_static_expander(title: str, path: Path, caption: str) -> None:
    with st.expander(title):
        show_static(path, caption)
