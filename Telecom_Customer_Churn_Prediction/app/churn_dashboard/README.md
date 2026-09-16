# Churn & Retention / Revenue & Geographic Performance Dashboard (Streamlit)

A Streamlit rebuild of the Power BI report (`PowerBI.pbix` / `dashboard.pdf`) —
same KPIs, charts, slicers, chart types, and charcoal/rose colour scheme,
laid out as 2 pages (same as the source report), deployed together under one link:

1. **Churn_And_Retention_Overview** (`Churn_And_Retention_Overview.py`) — main entry
2. **Revenue_And_Geographic_Performance** (`pages/2_Revenue_And_Geographic_Performance.py`)

## Files

```
churn_dashboard/
├── Churn_And_Retention_Overview.py            ← main entry (point Streamlit Cloud's "Main file path" here)
├── data.py                                    ← all chart/KPI numbers + colours, in one place
├── style.py                                    ← shared CSS (charcoal cards, rose KPI values)
├── requirements.txt
├── .streamlit/config.toml                     ← charcoal/rose theme
└── pages/
    └── 2_Revenue_And_Geographic_Performance.py
```

Streamlit names each sidebar entry after its filename, which is why the entry-point
file is named `Churn_And_Retention_Overview.py` (not `streamlit_app.py`) — so the
sidebar reads "Churn And Retention Overview" instead of a generic name.

## A note on the data

Every KPI, bar/donut/area/pie value was taken directly off the numbers printed
on the exported `dashboard.pdf`, so the values match exactly. The
**Contract_Type** (page 1) and **Payment_Method** (page 2, offer-based) slicers
are wired to actually filter their charts. **Internet_Service**, page-1
**Payment_Method**, and **City** are shown for layout parity but aren't
functional — the export has no underlying breakdown data for those.

The **Churn_Rate_By_City** world map is an illustrative reproduction only —
the source Bing Maps visual has no printed per-city values anywhere in the
PDF export, so exact bubble positions/sizes aren't recoverable; a caption on
that chart notes this.

If you'd rather have it pull live numbers, connect `data.py` to your actual
churn dataset (e.g. via SQLAlchemy/pandas) and swap the hardcoded DataFrames
for query results — the chart/layout code doesn't need to change.

## Deploy it — GitHub + Streamlit Community Cloud (free)

1. **Create a GitHub repo** (or a new folder in an existing one) and push this
   folder's contents to its root (so `Churn_And_Retention_Overview.py` sits at
   the repo root, not nested another level deep):
   ```bash
   cd churn_dashboard
   git init
   git add .
   git commit -m "Streamlit rebuild of churn/retention Power BI dashboard"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
2. Go to **https://share.streamlit.io** and sign in with GitHub.
3. Click **"New app"** → pick your repo → branch `main` → main file path
   `Churn_And_Retention_Overview.py` (or `churn_dashboard/Churn_And_Retention_Overview.py`
   if it's a subfolder of an existing repo) → **Deploy**.
4. Streamlit Cloud installs `requirements.txt` automatically and picks up
   `.streamlit/config.toml` for the theme — no extra config needed.
5. You'll get one public URL — both pages (Churn & Retention Overview,
   Revenue & Geographic Performance) live under it, switchable via the sidebar,
   exactly as asked.

Any time you `git push` an update, the deployed app redeploys automatically.

## Run it locally first (optional, to check before pushing)

```bash
pip install -r requirements.txt
streamlit run Churn_And_Retention_Overview.py
```
