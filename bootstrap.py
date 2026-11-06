"""Ensure `components` resolves whether pages live in streamlit_app/pages/ or pages/."""
from __future__ import annotations

import sys
from pathlib import Path


def ensure_streamlit_path() -> Path:
    """Return streamlit app root (directory that contains `components/`)."""
    here = Path(__file__).resolve().parent
    for p in (here, here.parent):
        if (p / "components").is_dir():
            if str(p) not in sys.path:
                sys.path.insert(0, str(p))
            return p
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))
    return here
