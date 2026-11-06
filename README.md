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

**Streamlit Community Cloud:** Point the app at **this repository root** (the folder that contains `Caucasus_Weather_Stations/` and `streamlit_app/`), with main file `streamlit_app/Home.py`. If only the `streamlit_app/` folder is deployed, the data directories will be missing.

## Structure

- `Home.py` — Home page (main entry)
- `pages/` — Multipage sections (Overview, Methods, Caucasus, Peru, Comparison, Conclusions)
- `components/` — Data loaders, charts, static figure helpers
