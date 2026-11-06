# Bundled data (CSV + reference PNGs)

These files are copies of the project's **derived** analysis outputs and **original figure PNGs** so the Streamlit app works on
**Streamlit Community Cloud** when the Git repository contains only the `streamlit_app` tree (no parent
`Caucasus_Weather_Stations/` folder).

**Regenerate locally** from the full project after updating analyses:

```bash
python streamlit_app/scripts/bundle_data.py
```

Commit changes under `streamlit_app/data/` so deployments stay in sync.

**Alternative layout:** you may place the same filenames directly under `Caucasus_Weather_Stations/` (not only under `derived/`); the app checks both.
