# Churn & Retention / Revenue & Geographic Dashboard (Streamlit)

> **v2 fixes:** (1) The `Churn_Rate_By_City` map no longer uses
> `px.scatter_mapbox` (that call depends on internals that differ across
> plotly/pandas versions and threw an `AttributeError` on Streamlit Cloud's
> resolved package versions). It now uses a plain `go.Scattergeo` map, which
> needs no Mapbox token and works identically across versions. (2) Package
> versions are now pinned exactly in `requirements.txt` so Streamlit Cloud
> can't resolve a mismatched combo again. (3) The entry file was renamed from
> `app.py` to `Churn_And_Retention_Overview.py` so the sidebar shows a real
> dashboard name instead of the literal word "app".

A pixel-matched Streamlit re-build of your Power BI report (`PowerBI.pbix`),
with **both pages published at one link**:

1. **Churn_And_Retention_Overview** — `Churn_And_Retention_Overview.py` (home page)
2. **Revenue_And_Geographic_Performance** — `pages/1_Revenue_And_Geographic_Performance.py`

Streamlit's built-in multipage navigation gives you both dashboards in the
sidebar of a single deployed app — exactly like the two tabs in your `.pbix`.

## What was kept identical to the source dashboard

- **KPIs**: `Total_Customers`, `Churn_Rate_In_Per`, `Avg_Tenure_In_Per`,
  `Churned_Customers`, `Total_Revenue`, `Average_CLTV_In_Per`, `Revenue_By_Offer`
  — computed with the *exact* DAX logic extracted from your `.pbix` data
  model (`DISTINCTCOUNT`, `Churn_Rate = Churned/Total*100`,
  `Avg_CLTV = AVERAGE(Total Revenue)`, etc.)
- **Calculated columns**: `Tenure_Band`, `Referral_Band`, `Population_Density`
  — copied verbatim from the model's DAX (0-12/12-24/24-48/48+ months,
  0/1-3/4+ referrals, <10K/10K-50K/50K+ population).
- **All charts, slicers, and chart types**:
  - Churn_Rate_By_Contract (column)
  - Top_5_Churn_Reason_For_Churn (donut)
  - Churn_Rate_By_Tenure_Band (area)
  - Churn_Rate_By_Internet_Type (bar)
  - Churn_Rate_By_City (map)
  - Churn_Rate_By_Number_Of_Referrals (bar)
  - Churn_Rate_By_Offer (column)
  - Churn_Rate_By_Population_Density (pie)
  - Slicers: `Contract_Type`, `Internet_Service`, `Payment_Method`, `City`, `Offer`
  - `Clear_All_Slicers` button
- **Colors**: dark theme + rose accent `#DE6A73` (extracted directly from the
  `.pbix` visual definitions) with the same alternating accent/white bar
  pattern used in the original report.

All numbers were verified against the KPI values shown in your PDF export
(7K customers, 26.54% churn, 32.39 avg tenure, 21.37M revenue, 3.03K CLTV,
10.02M revenue by offer, etc.) and match exactly.

> Note: the `.pbix` file itself cannot be read by Streamlit or any web app —
> Power BI files only open in Power BI Desktop/Service. This app was built by
> reverse-engineering the `.pbix` (DAX measures, calculated columns, colors,
> chart types) and re-implementing the same logic against your CSV extracts,
> so the published Streamlit app looks and calculates identically.

## Files

```
.
├── Churn_And_Retention_Overview.py         # Page 1: Churn & Retention
├── pages/
│   └── 1_Revenue_And_Geographic_Performance.py      # Page 2: Revenue & Geographic
├── utils.py                                         # shared data prep + theme
├── data/                                            # the 5 CSVs you provided
├── requirements.txt
├── .streamlit/config.toml                           # dark theme colors
└── README.md
```

## 1. Push to GitHub

```bash
cd churn-dashboard
git init
git add .
git commit -m "Churn & retention / revenue & geographic Streamlit dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

(Or just create a new repo on github.com, then drag-and-drop / upload all
these files and folders through the GitHub web UI — no CLI needed.)

## 2. Deploy on Streamlit Community Cloud

1. Go to **https://share.streamlit.io** and sign in with GitHub.
2. Click **"New app"**.
3. Pick your repo, branch `main`, and main file path **`Churn_And_Retention_Overview.py`**.
4. Click **Deploy**.

That's it — Streamlit auto-installs `requirements.txt`, and both dashboard
pages appear under one URL, switchable from the sidebar (`app` /
`Revenue And Geographic Performance`).

## 3. Run locally first (optional, to check before pushing)

```bash
pip install -r requirements.txt
streamlit run Churn_And_Retention_Overview.py
```

Open the printed local URL — you'll see both pages in the left sidebar.

## Customizing further

- Slicers live in the `with st.sidebar:` block at the top of each page file.
- Colors are all defined once in `utils.py` (`ACCENT`, `SECONDARY`,
  `DONUT_PALETTE`, `DENSITY_PALETTE`, `BG_COLOR`, `PANEL_BG`) — change them
  there and every chart/KPI updates.
- Chart building blocks (`kpi_card`, `panel_start`/`panel_end`, `base_layout`,
  `alt_colors`) are reusable helpers, also in `utils.py`.
