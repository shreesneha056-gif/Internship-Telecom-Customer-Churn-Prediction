# Telecom Customer Churn Prediction — Analytics Project

> **End-to-end telecom analytics solution combining SQL, Power BI, Python predictive modeling, and Streamlit deployment.**

[![Dashboard](https://img.shields.io/badge/Live-Churn%20Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://telecom-customer-churn-prediction-analysis-dashboard.streamlit.app/)
[![Predictive Analysis](https://img.shields.io/badge/Live-Predictive%20Analysis-blueviolet?logo=streamlit&logoColor=white)](https://telecom-project-customer-churn-predictive-analysis.streamlit.app/)

## Project Overview

This project was developed to build a **data-driven churn analysis and retention solution for a telecom business**, enabling stakeholders to understand churn drivers, identify at-risk customers, and take proactive retention actions.

The solution brings together data validation, exploratory and diagnostic analysis, interactive dashboards, predictive machine-learning models, and live Streamlit applications into one analytics pipeline.

### Objectives

- Build stakeholder-focused dashboards tracking churn and revenue performance
- Analyze customer demographics, services, contracts, and geography
- Identify churn drivers across tenure, internet type, contract type, and offers
- Predict customer churn probability
- Predict customer revenue
- Segment customers into behavioral clusters
- Predict the best retention offer for each customer
- Turn analytical findings into actionable business recommendations

## Live Applications

| Application | Purpose | Link |
|---|---|---|
| **Dashboard App** | Interactive churn, retention, and revenue dashboards | [Open Dashboard](https://telecom-customer-churn-prediction-analysis-dashboard.streamlit.app/) |
| **Predictive Analysis App** | Churn probability, revenue prediction, segmentation, and best offer | [Open Predictive Analysis](https://telecom-project-customer-churn-predictive-analysis.streamlit.app/) |

Both applications are publicly accessible without login and are designed for stakeholder self-service.

## Data

The project uses five core tables:

| Table | Description |
|---|---|
| `customer_account_status.csv` | Contract type, tenure, charges, payment method |
| `customer_demographics.csv` | Age, gender, dependents, senior citizen status |
| `customer_location.csv` | City, state, latitude, longitude, zip code |
| `customer_services.csv` | Internet type, phone, streaming, tech support services |
| `zipcode_population.csv` | Population density by zip code |

**Coverage:** 7,043 telecom customers — California region

### Data Quality Checks

SQL was used to audit the data before analysis and modeling, including:

- Primary-key uniqueness
- Duplicate detection
- Referential-integrity / orphan-row checks
- Missing-value checks
- Business-rule validation

## Analytics Workflow

```text
Raw Telecom Customer Data (5 CSVs)
        |
        v
   SQL Server
   Data Audit & Validation
        |
        +-------------------+
        |                   |
        v                   v
       EDA             KPI / Churn Analysis
        |                   |
        +---------+---------+
                  |
          Power BI Dashboards
                  |
                  v
        Python Predictive Models (4 Models)
                  |
                  v
          Streamlit Applications
```

## Technology Stack

- **SQL Server** — data import, auditing, KPI definitions, churn analysis, geographic performance
- **Power BI** — interactive dashboard design and business visualization
- **Python** — EDA, feature engineering, predictive modeling, and segmentation
- **Streamlit** — deployment of stakeholder-facing analytical applications
- **Pandas / NumPy** — data preparation and numerical analysis
- **Scikit-learn** — K-Means clustering and preprocessing
- **XGBoost** — churn prediction, revenue prediction, and best offer prediction
- **Plotly** — interactive charts and geographic maps

## Power BI Dashboards

### 1. Churn & Retention Overview

Key KPIs and views include:

- Total Customers (7K)
- Churn Rate (26.54%)
- Churned Customers (2K)
- Avg Tenure (32.39 months)
- Churn Rate by Contract Type
- Churn Rate by Tenure Band
- Churn Rate by Internet Type
- Top 5 Churn Reasons (donut chart)
- Churn Rate by Population Density

### 2. Revenue & Geographic Performance

Key metrics include:

- Total Revenue (21.37M)
- Average CLTV (3.03K)
- Revenue by Offer
- Churn Rate by Number of Referrals
- Churn Rate by Offer Type
- Customer Geographic Map (city-level, California)

## Key Business Results

### Churn & Retention

- **7,043** total customers
- **26.54%** overall churn rate
- **1,869** churned customers
- **32.39 months** average tenure
- Month-to-month contracts had the highest churn rate at **46%**
- Fiber Optic internet customers churned at **41%** vs DSL at **19%**
- Customers with 0 referrals churned at **36%** vs loyal referrers at **4%**
- Offer E had the lowest churn rate at **7%** vs no-offer customers at **53%**

### Revenue & Geography

- **$21.37M** total revenue
- **$3.03K** average customer lifetime value (CLTV)
- **$10.02M** revenue from customers on Offer type
- Top churn reasons: Competitor offer (28.69%), Competitor device (28.51%), Attitude (20.16%)
- Dataset covers California cities — San Diego, Los Angeles, San Francisco and more

## Predictive Analytics

Four production-oriented models were developed and deployed:

### Model 1 — Churn Prediction

**Business question:** Will this customer churn?

- Problem type: Binary classification
- Base churn rate: **26.54%**
- Best model: **XGBoost Classifier**
- **ROC-AUC: 0.90**
- Key drivers: Contract type, tenure, internet type, number of referrals, offer type

### Model 2 — Revenue Prediction

**Business question:** How much revenue will this customer generate?

- Problem type: Regression
- Best model: **XGBoost Regressor**
- **R²: 0.83 | MAE: $867.59**
- Inputs: Customer services, tenure, contract type, demographics

### Model 3 — Customer Segmentation

**Business question:** Which behavioral segment does this customer belong to?

- Problem type: Unsupervised clustering
- Best model: **K-Means (K=5)**
- Cluster sizes: 897 / 2,498 / 2,591 / 973 / 84 customers
- Used to identify high-risk, high-value, and loyal customer groups

### Model 4 — Best Offer Prediction

**Business question:** Which retention offer best reduces this customer's churn risk?

- Problem type: Multi-class classification + offer simulation
- Best model: **XGBoost Classifier**
- **ROC-AUC: 0.90**
- Simulates all 6 offer scenarios (No Offer, A–E) and recommends the one that minimizes predicted churn
- Depends on Model 3 cluster as an input feature

## Key Insights

1. **Contract type is the strongest churn lever:** month-to-month customers churn at 4× the rate of two-year contract customers.
2. **Fiber Optic customers churn at twice the rate of DSL:** service quality or pricing issues may be driving dissatisfaction.
3. **Referrals are a strong retention signal:** customers with no referrals churn at 36%, dropping to near 4% for highly-referred customers.
4. **Offer E is the most effective retention tool:** reducing churn from 53% (no offer) to just 7%.
5. **Competitor offers and devices are the top churn triggers:** accounting for over 57% of churn reasons.
6. **High CLTV customers warrant proactive intervention:** average CLTV of $3.03K means each retained customer has significant revenue value.

## Recommendations

- Migrate month-to-month customers to longer-term contracts with incentives.
- Investigate Fiber Optic service quality and pricing to address the high churn rate.
- Expand referral programs to increase the number of customer-referred customers.
- Deploy **Offer E** as the default retention offer for at-risk customers identified by the churn model.
- Use the **predictive app** to score individual customers and personalise retention campaigns.
- Monitor CLTV and segment-level churn rates monthly using the dashboard.

## Repository Structure

```text
Internship-Telecom-Customer-Churn-Prediction/
├── Telecom_Customer_Churn_Prediction/
│   ├── app/
│   │   ├── churn_dashboard/     # Streamlit dashboard app (2 pages)
│   │   └── predictive_app/      # Streamlit predictive analytics app (4 models)
│   ├── dashboard/
│   │   ├── PowerBI.pbix         # Original Power BI report
│   │   └── dashboard.pdf        # Dashboard PDF export
│   ├── data/                    # 5 raw customer CSV files
│   ├── eda/                     # 4 model notebooks (EDA + training)
│   │   ├── Model_1_Churn_Prediction.ipynb
│   │   ├── Model_2_Revenue_Prediction.ipynb
│   │   ├── Model_3_Customer_Segmentation.ipynb
│   │   └── Model_4_Best_Offer_Prediction.ipynb
│   └── sql/
│       └── SQL.sql              # Data audit & KPI queries
└── README.md
```

## Assumptions & Limitations

- Dataset covers **California customers only** — results and geographic maps reflect this scope.
- Currency is assumed to be **USD** for all revenue and CLTV fields.
- Model 3 (K-Means) scaler is bundled with the KMeans object in `segmentation_model.pkl` to ensure consistent live scoring.
- Model 4 depends on Model 3 output (cluster label) as an input feature.
- Refund and session-level data were not available for this dataset.

## Business Value

This project demonstrates a complete analytics lifecycle:

**Data Validation → SQL Analysis → BI Dashboards → Predictive Modeling → Segmentation → Streamlit Deployment → Business Recommendations**

The result is a stakeholder-ready analytics package that combines validated data, interactive dashboards, 4 predictive models, and actionable retention insights.

## Author

**Sneha Shree M U**

Telecom Customer Churn Prediction — Internship Analytics Project

---

### Live Demo

- 📊 [Dashboard Application](https://telecom-customer-churn-prediction-analysis-dashboard.streamlit.app/)
- 🤖 [Predictive Analysis Application](https://telecom-project-customer-churn-predictive-analysis.streamlit.app/)
