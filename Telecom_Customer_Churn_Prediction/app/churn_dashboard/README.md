# Churn & Retention / Revenue & Geographic Performance Dashboard

A 2-page Streamlit recreation of the Power BI report (`PowerBI.pbix`), rebuilt from the
underlying CSVs and styled to match the original PDF export (`dashboard.pdf`) — same KPIs,
same charts, same chart types, same colour palette, same slicers.

> **Why not just deploy the `.pbix`?** Streamlit (and Python generally) cannot open or render
> `.pbix` files — it's a proprietary Power BI binary format. The only way to get this report
> on Streamlit is to rebuild the visuals from the source data, which is what this app does.
> All chart values were verified against your PDF and match exactly (7,043 customers, 26.54%
> churn rate, 21.37M revenue, etc.).

## Pages
1. **Home.py** → `Churn_And_Retention_Overview` (KPIs, Churn by Contract, Top 5 Churn
   Reasons, Churn by Tenure Band, Churn by Internet Type + Contract/Internet Service/Payment
   Method slicers)
2. **pages/1_Revenue_And_Geographic_Performance.py** → `Revenue_And_Geographic_Performance`
   (KPIs, Churn by City map, Churn by Referrals, Churn by Offer, Churn by Population Density
   + City/Offer slicers)

Both pages are part of **one Streamlit app** — Streamlit's built-in multipage navigation
(sidebar) lets you switch between them from a single deployed URL.

## Project structure
```
streamlit_dashboard/
├── Home.py                                        # Page 1 (entry point)
├── pages/
│   └── 1_Revenue_And_Geographic_Performance.py     # Page 2
├── utils.py                                        # shared data loading + theme
├── data/
│   ├── customer_account_status.csv
│   ├── customer_demographics.csv
│   ├── customer_location.csv
│   ├── customer_services.csv
│   └── zipcode_population.csv
├── requirements.txt
└── README.md
```

## 1. Push to GitHub
```bash
cd streamlit_dashboard
git init
git add .
git commit -m "Churn & retention Streamlit dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```
(Or just create a new repo on github.com, upload these files/folders via the web UI —
make sure `data/` and `pages/` keep their folder structure.)

## 2. Deploy on Streamlit Community Cloud
1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **"New app"**.
3. Pick your repository and branch (`main`).
4. Set **Main file path** to `Home.py`.
5. Click **Deploy**.

Streamlit auto-detects `requirements.txt` and installs `streamlit`, `pandas`, `plotly`.
The `pages/` folder is auto-discovered — no extra config needed. You'll get one URL
(e.g. `https://your-app.streamlit.app`) with both report pages accessible from the
sidebar nav.

## Notes on data-derived values
- **Revenue_By_Offer** = total revenue of customers who have any offer (i.e. excludes
  "No Offer") — this is what reproduces the 10.02M figure in your PDF.
- **Average_CLTV_In_Per** = average `Total Revenue` per customer (≈3.03K, matches PDF).
- **Churn_Rate_By_Population_Density** pie = each density band's churn rate expressed as a
  share of the three bands' combined churn rate (this is what reproduces the
  36.79% / 33.52% / 29.69% split in your PDF).
- All slicers filter both the KPIs and every chart on their page, live, like Power BI.

## Customizing
- Colours/fonts live in `utils.py` (`ROSE`, `ROSE_DARK`, `GRAY_BAR`, `DONUT_COLORS`, etc.)
- Nothing about the layout, chart types, KPI cards, or slicers was changed from the
  original PDF — this is a 1:1 structural recreation of the two report pages.
