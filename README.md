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

## Structure

- `Home.py` — Home page (main entry)
- `pages/` — Multipage sections (Overview, Methods, Caucasus, Peru, Comparison, Conclusions)
- `components/` — Data loaders, charts, static figure helpers
