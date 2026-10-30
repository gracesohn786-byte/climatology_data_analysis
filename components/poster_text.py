"""Poster extract helpers."""
from __future__ import annotations

from pathlib import Path


def extract_abstract(extract_path: Path) -> str | None:
    if not extract_path.is_file():
        return None
    text = extract_path.read_text(encoding="utf-8", errors="replace")
    start = text.find("Abstract")
    if start < 0:
        return None
    start += len("Abstract")
    end = text.find("Methods", start)
    if end < 0:
        end = len(text)
    block = text[start:end].strip()
    lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
    return " ".join(lines) if lines else None
