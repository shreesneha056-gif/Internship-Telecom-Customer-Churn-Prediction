"""
Loads and merges the real Telco customer churn CSVs, and computes every
derived column the dashboard's charts need (tenure band, referral band,
population density band, churn flag, etc).

All KPI/chart numbers in the app are computed live from this dataframe,
filtered by whatever slicers are currently active — this is what makes the
slicers genuinely cross-filter every chart, not just one.
"""
import os
import pandas as pd
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def _tenure_band(months):
    if months < 12:
        return "0-12 months"
    elif months < 24:
        return "12-24 months"
    elif months < 48:
        return "24-48 months"
    return "48+ months"


def _referral_band(n):
    if n == 0:
        return "0_Referral"
    elif n <= 3:
        return "1-3_Referral"
    return "4+_Referral"


def _density_band(pop):
    if pd.isna(pop):
        return None
    if pop >= 50000:
        return "High density (50K+)"
    elif pop >= 10000:
        return "Medium density (10K-50K)"
    return "Low density (<10K)"


@st.cache_data
def load_data():
    acct = pd.read_csv(os.path.join(DATA_DIR, "customer_account_status.csv"))
    loc = pd.read_csv(os.path.join(DATA_DIR, "customer_location.csv"))
    svc = pd.read_csv(os.path.join(DATA_DIR, "customer_services.csv"))
    zpop = pd.read_csv(os.path.join(DATA_DIR, "zipcode_population.csv"))

    df = acct.merge(loc, on="Customer ID", how="left")
    df = df.merge(svc, on="Customer ID", how="left")
    df = df.merge(zpop, on="Zip Code", how="left")

    df["churned"] = (df["Customer Status"] == "Churned").astype(int)
    df["Internet Type"] = df["Internet Type"].fillna("No Internet Service")
    df["has_internet"] = (df["Internet Type"] != "No Internet Service").map({True: "True", False: "False"})
    df["Offer"] = df["Offer"].fillna("No Offer")
    df["tenure_band"] = df["Tenure in Months"].apply(_tenure_band)
    df["referral_band"] = df["Number of Referrals"].apply(_referral_band)
    df["density_band"] = df["Population"].apply(_density_band)

    return df


TENURE_ORDER = ["0-12 months", "12-24 months", "24-48 months", "48+ months"]
CONTRACT_ORDER = ["Month-to-Month", "One Year", "Two Year"]
REFERRAL_ORDER = ["1-3_Referral", "0_Referral", "4+_Referral"]
OFFER_ORDER = ["Offer E", "No Offer", "Offer D", "Offer C", "Offer B", "Offer A"]
DENSITY_ORDER = ["High density (50K+)", "Medium density (10K-50K)", "Low density (<10K)"]


def churn_rate_by(df, groupcol, order=None):
    """Plain churn rate (%) within each group, rounded to whole numbers —
    matches how Churn_Rate_By_Contract / _Internet_Type / _Offer / _Referrals
    are computed in the source report."""
    if df.empty:
        return pd.Series(dtype=float)
    rates = (df.groupby(groupcol)["churned"].mean() * 100).round(0).astype(int)
    if order:
        rates = rates.reindex([o for o in order if o in rates.index])
    return rates


def top5_churn_reason_pie(df):
    """Top-5 churn reasons among churned customers, renormalized so the
    5 shares sum to 100% — matches the source report's donut."""
    churned = df[df["churned"] == 1]
    if churned.empty:
        return pd.Series(dtype=float)
    counts = churned["Churn Reason"].value_counts().head(5)
    return (counts / counts.sum() * 100).round(2)


def density_churn_pie(df):
    """Churn rate per population-density band, renormalized so the bands
    sum to 100% — matches the source report's donut."""
    if df.empty:
        return pd.Series(dtype=float)
    sub = df.dropna(subset=["density_band"])
    rates = sub.groupby("density_band")["churned"].mean() * 100
    if rates.sum() == 0:
        return rates
    return (rates / rates.sum() * 100).round(2).reindex([o for o in DENSITY_ORDER if o in rates.index])
