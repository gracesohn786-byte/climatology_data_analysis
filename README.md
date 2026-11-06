# Weather Stations Analysis — Streamlit Research Presentation

Interactive research presentation for lapse rate and freezing level analyses (Caucasus and Peru).

## Setup

From the **repository root** (parent of `streamlit_app/`):

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r streamlit_app/requirements.txt
```

## Run

```bash
streamlit run streamlit_app/Home.py
```

The app reads existing derived CSVs and PNGs under `Caucasus_Weather_Stations/`, `Senamhi_Weather_Stations/`, and `Peru_Lascar_EDW_temperature_humidity/`. It does not modify those files.

**Streamlit Community Cloud**

1. **Preferred:** Main file `streamlit_app/Home.py`. Repo can be the **whole** data-analysis folder *or* only `streamlit_app/`.
2. **Data:** If the repo has **no** `Caucasus_Weather_Stations/derived/` at the parent level, the app reads CSVs from **`streamlit_app/data/`** (committed copies). Refresh them after re-running analyses:

   `python streamlit_app/scripts/bundle_data.py`

3. **Dependencies:** If the Git repo root is the **whole** project folder, `requirements.txt` at that root matches `streamlit_app/requirements.txt`. If you deploy **only** the app folder as the repo root, keep the same `requirements.txt` contents at repo root (Streamlit Cloud always runs `pip install` from the repo root).

## Structure

- `Home.py` — Home page (main entry)
- `pages/` — Multipage sections (Overview, Methods, Caucasus, Peru, Comparison, Conclusions)
- `components/` — Data loaders, charts, static figure helpers
