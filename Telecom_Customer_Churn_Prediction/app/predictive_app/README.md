# Telecom Customer Analytics — Live Predictions (Streamlit)

A single Streamlit app covering all 4 of your models:

1. **Churn Prediction** (`Model_1_Churn_Prediction.ipynb`) — XGBoost classifier, ROC-AUC 0.90
2. **Revenue Prediction** (`Model_2_Revenue_Prediction.ipynb`) — XGBoost regressor, R² 0.83
3. **Customer Segmentation** (`Model_3_Customer_Segmentation.ipynb`) — K-Means, K=5
4. **Best Offer Prediction** (`Model_4_Best_Offer_Prediction.ipynb`) — XGBoost classifier + offer simulation, ROC-AUC 0.90

You fill in one customer profile at the top of the app, then use any of the 4 tabs
below it to get that customer's churn probability, predicted revenue, behavioral
segment, or the offer that most reduces their churn risk.

## Files

```
predictive_app/
├── app.py                                     ← the Streamlit app (shared profile form + 4 tabs)
├── requirements.txt
├── .streamlit/config.toml                     ← dark rose theme
└── models/
    ├── churn_model.pkl                        ← Model 1 (XGBClassifier)
    ├── churn_model_columns.pkl
    ├── revenue_model.pkl                      ← Model 2 (XGBRegressor)
    ├── revenue_model_columns.pkl
    ├── segmentation_model.pkl                 ← Model 3 (dict: {"scaler","kmeans","feature_order"})
    ├── cluster_profile.csv                    ← per-segment averages, shown in the Segmentation tab
    ├── best_offer_churn_model.pkl             ← Model 4 (XGBClassifier)
    ├── best_offer_model_columns.pkl
    └── best_offer_by_segment.csv
```

## How the model files were produced

Your 4 notebooks were Databricks notebooks (they read from
`/Volumes/workspace/default/raw_data/...` and write their `.pkl` outputs back
there), so the trained models only existed inside that Databricks workspace —
not as portable files. I re-ran each notebook's exact pipeline — same cleaning
and merge steps, same one-hot/binary encoding, same VIF-selected feature list,
same `random_state=123` splits, same final model each notebook's own
comparison table landed on (XGBoost won Models 1, 2, and 4; K-Means with K=5
for Model 3) — against your uploaded CSVs, and verified each result:

| Model | Metric here | Notebook's own reported result |
|---|---|---|
| 1. Churn (XGBoost) | Test ROC-AUC 0.900 | grid search picked the same params, ROC-AUC ~0.90 |
| 2. Revenue (XGBoost) | Test R² 0.826, MAE $867.59 | grid search picked the same params |
| 3. Segmentation (K-Means, K=5) | 5 well-separated clusters (897 / 2,498 / 2,591 / 973 / 84 customers) | same K, same feature set |
| 4. Best Offer (XGBoost) | Test ROC-AUC 0.901 | same pipeline, adds Model 3's cluster as a feature |

**One gap I filled in:** Model 3's notebook fits a `StandardScaler` on the
segmentation features but never saves it — only the fitted `KMeans` gets
dumped to disk. That's fine for labeling the *training* customers, but a live
app scoring a *new* customer needs that exact same fitted scaler to transform
their inputs consistently before calling `kmeans.predict()`. So
`segmentation_model.pkl` here bundles `{"scaler", "kmeans", "feature_order"}`
instead of just the bare K-Means object.

**Model 4 depends on Model 3:** the "Best Offer Prediction" tab first runs the
customer through the segmentation model to get their cluster, then feeds that
cluster (as `Cluster_1`..`Cluster_4` dummies) into the offer model alongside
their other features, and simulates all 6 offer scenarios (No Offer, A–E) to
find whichever minimizes predicted churn — exactly as the notebook's own
simulation cells do, just for one live customer instead of the whole base.

## Deploy it — GitHub + Streamlit Community Cloud (free)

1. Push this folder's contents to a GitHub repo (its own repo, or a new
   subfolder in an existing one — keep it separate from your dashboard app):
   ```bash
   cd predictive_app
   git init
   git add .
   git commit -m "Telecom predictive analytics Streamlit app"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
2. Go to **https://share.streamlit.io** → **New app** → pick the repo/branch →
   **Main file path** `app.py` (or `predictive_app/app.py` if it's nested in
   an existing repo) → **Deploy**.
3. You'll get a public URL — this is your "predictive model + web app link"
   deliverable, separate from the dashboard's URL.

## Run it locally first (optional)

```bash
pip install -r requirements.txt
streamlit run app.py
```
