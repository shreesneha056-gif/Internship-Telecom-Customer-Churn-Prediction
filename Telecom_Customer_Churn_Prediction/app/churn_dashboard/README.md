# Churn & Retention / Revenue & Geographic Performance Dashboard (Streamlit)

A Streamlit rebuild of the Power BI report (`PowerBI.pbix` / `dashboard.pdf`).

**This version is fully data-driven** — every KPI and chart is computed live
from the real Telco customer CSVs (`data/` folder), not hardcoded from the
PDF. That's what makes the slicers genuinely cross-filter every chart, not
just one: each page filters the underlying dataframe once, and every
KPI/chart on that page recomputes from the same filtered slice.

Deployed as 2 pages under one link, same as the source report:

1. **Churn_And_Retention_Overview** (`Churn_And_Retention_Overview.py`) — main entry
2. **Revenue_And_Geographic_Performance** (`pages/2_Revenue_And_Geographic_Performance.py`)

## Files

```
churn_dashboard/
├── Churn_And_Retention_Overview.py            ← main entry (point Streamlit Cloud's "Main file path" here)
├── data_loader.py                             ← loads/merges the real CSVs, computes every derived column
├── data.py                                    ← color/theme constants only
├── style.py                                   ← shared CSS (charcoal cards, rose KPI values)
├── requirements.txt
├── .streamlit/config.toml                     ← charcoal/rose theme
├── data/                                      ← the 5 real CSVs (~1.7MB total)
│   ├── customer_account_status.csv
│   ├── customer_demographics.csv
│   ├── customer_location.csv
│   ├── customer_services.csv
│   └── zipcode_population.csv
└── pages/
    └── 2_Revenue_And_Geographic_Performance.py
```

## What changed from the previous version, and why

**1. Real cross-filtering, not one chart at a time.** Previously each chart
had its own hardcoded numbers (read off the PDF), so a slicer could only
plausibly filter the one chart it was written to touch. Now every page loads
the merged customer-level dataframe, applies *all* active slicers to it in
one filter step, and every KPI/chart on that page is computed from that same
filtered dataframe. Selecting "One Year" in `Contract_Type`, for example, now
correctly shrinks the customer base for the KPIs, the tenure/internet/reason
charts, everything downstream — not just the contract chart itself.

**2. Churn_Rate_By_Tenure_Band** was previously a flat single-color area
fill. It's now alternating maroon/grey bars (0-12mo / 24-48mo maroon,
12-24mo / 48+mo grey) with a white line-and-markers trace on top, matching
the source chart's actual look.

**3. Churn_Rate_By_City** was previously a rough illustrative world map,
because the PDF export gives no printed per-city numbers to work from. With
the real `customer_location.csv` (which has exact latitude/longitude per
customer) now available, the map is built from real data: it's a proper
scatter-geo of actual customer cities, bubble size = customer count, color =
churn rate. One thing worth flagging: **this dataset is California-only** —
every city in `customer_location.csv` is a CA city (San Diego, Los Angeles,
San Francisco, etc.). The original PDF's map showed blobs scattered across
North America, Europe, Asia, and Australia, which doesn't match this
data — that appears to have been a geocoding mismatch in the source Power BI
report itself (Bing Maps likely mis-resolved some city names against
non-US places of the same name). This rebuild plots the real coordinates
instead of reproducing that apparent error, and auto-zooms to fit the actual
data (California) via `fitbounds="locations"`.

## Verified against the source PDF

Every KPI and chart value computed from the real CSVs (unfiltered) matches
the numbers printed in the original PDF exactly:

| Metric | Computed here | Source PDF |
|---|---|---|
| Total_Customers | 7,043 → 7K | 7K |
| Churn_Rate_In_Per | 26.54 | 26.54 |
| Avg_Tenure_In_Per | 32.39 | 32.39 |
| Churned_Customers | 1,869 → 2K | 2K |
| Churn_Rate_By_Contract | 46 / 11 / 3 | 46 / 11 / 3 |
| Churn_Rate_By_Tenure_Band | 48 / 30 / 21 / 10 | 48 / 30 / 21 / 10 |
| Churn_Rate_By_Internet_Type | 41 / 26 / 19 / 7 | 41 / 26 / 19 / 7 |
| Total_Revenue | 21.37M | 21.37M |
| Average_CLTV_In_Per | 3.03K | 3.03K |
| Revenue_By_Offer | 10.02M | 10.02M |
| Churn_Rate_By_Number_Of_Referrals | 36 / 33 / 4 | 36 / 33 / 4 |
| Churn_Rate_By_Offer | 53 / 27 / 27 / 23 / 12 / 7 | 53 / 27 / 27 / 23 / 12 / 7 |
| Top_5_Churn_Reason (donut) | 28.69 / 28.51 / 20.16 / 11.92 / 10.72 | same |
| Churn_Rate_By_Population_Density (donut) | 36.79 / 33.52 / 29.69 | same |

## Deploy it — GitHub + Streamlit Community Cloud (free)

1. Push this folder's contents to a GitHub repo root (so
   `Churn_And_Retention_Overview.py` sits at the repo root, or note the
   subfolder path if it's nested inside an existing repo):
   ```bash
   cd churn_dashboard
   git init
   git add .
   git commit -m "Data-driven Streamlit rebuild of churn/retention dashboard"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
2. Go to **https://share.streamlit.io** → **New app** → pick the repo/branch →
   main file path `Churn_And_Retention_Overview.py` (or the subfolder path,
   e.g. `churn_dashboard/Churn_And_Retention_Overview.py`) → **Deploy**.
3. Streamlit Cloud installs `requirements.txt` and picks up
   `.streamlit/config.toml` for the theme automatically. The `data/` folder
   ships with the repo, so no separate database or upload step is needed.
4. One public URL, both pages switchable via the sidebar.

## Run it locally first (optional)

```bash
pip install -r requirements.txt
streamlit run Churn_And_Retention_Overview.py
```
