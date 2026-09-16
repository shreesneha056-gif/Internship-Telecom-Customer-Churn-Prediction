"""
Shared data loading, feature engineering, and theme constants for the
Churn & Retention / Revenue & Geographic Performance Streamlit dashboards.
"""
import pandas as pd
import streamlit as st

# ----------------------------- THEME / COLORS -----------------------------
BG_COLOR = "#0e0e11"
CARD_COLOR = "#1a1a1f"
BORDER_COLOR = "#2b2b31"
TEXT_WHITE = "#f5f5f5"
TEXT_GRAY = "#b3b3b3"
ROSE = "#d17a92"          # primary accent bar color
ROSE_DARK = "#7a2e3d"     # maroon (tenure band)
WHITE_BAR = "#ffffff"
GRAY_BAR = "#8c8c8c"

DONUT_COLORS = ["#7a3b2e", "#b3542f", "#d17a92", "#c98f6b", "#e8d9cf"]
DENSITY_COLORS = ["#ffffff", "#d17a92", "#7a2e3d"]

PLOTLY_LAYOUT = dict(
    paper_bgcolor=CARD_COLOR,
    plot_bgcolor=CARD_COLOR,
    font=dict(color=TEXT_WHITE, size=13),
    margin=dict(l=10, r=10, t=30, b=10),
)

CARD_CSS = f"""
<style>
.stApp {{
    background-color: {BG_COLOR};
}}
[data-testid="stSidebar"] {{
    background-color: {CARD_COLOR};
    border-right: 1px solid {BORDER_COLOR};
}}
.block-container {{
    padding-top: 1.2rem;
}}
.dash-title {{
    background-color: #000000;
    color: white;
    text-align: center;
    font-size: 26px;
    padding: 14px 0;
    border-radius: 4px;
    margin-bottom: 18px;
    letter-spacing: 1px;
}}
.kpi-card {{
    background-color: {CARD_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 14px 18px;
    text-align: left;
}}
.kpi-label {{
    color: {ROSE};
    font-size: 13px;
    font-weight: 500;
}}
.kpi-value {{
    color: {TEXT_WHITE};
    font-size: 26px;
    font-weight: 700;
}}
.chart-card {{
    background-color: {CARD_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 10px 14px 4px 14px;
    margin-bottom: 16px;
}}
.chart-title {{
    color: {TEXT_WHITE};
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 4px;
}}
</style>
"""


def inject_css():
    st.markdown(CARD_CSS, unsafe_allow_html=True)


def kpi_card(label, value):
    st.markdown(
        f"""<div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>""",
        unsafe_allow_html=True,
    )


def chart_title(title):
    st.markdown(f'<div class="chart-title">{title}</div>', unsafe_allow_html=True)


def page_title(title):
    st.markdown(f'<div class="dash-title">{title}</div>', unsafe_allow_html=True)


# ----------------------------- DATA LOADING -----------------------------
DATA_DIR = "data"


@st.cache_data
def load_data():
    acc = pd.read_csv(f"{DATA_DIR}/customer_account_status.csv")
    demo = pd.read_csv(f"{DATA_DIR}/customer_demographics.csv")
    loc = pd.read_csv(f"{DATA_DIR}/customer_location.csv")
    serv = pd.read_csv(f"{DATA_DIR}/customer_services.csv")
    pop = pd.read_csv(f"{DATA_DIR}/zipcode_population.csv")

    df = acc.merge(demo, on="Customer ID", how="left")
    df = df.merge(loc, on="Customer ID", how="left")
    df = df.merge(serv, on="Customer ID", how="left")
    df = df.merge(pop, on="Zip Code", how="left")

    df["Is_Churned"] = (df["Customer Status"] == "Churned").astype(int)

    df["Tenure_Band"] = pd.cut(
        df["Tenure in Months"],
        bins=[-1, 12, 24, 48, 1000],
        labels=["0-12 months", "12-24 months", "24-48 months", "48+ months"],
    )

    df["Referral_Band"] = pd.cut(
        df["Number of Referrals"],
        bins=[-1, 0, 3, 1000],
        labels=["0_Referral", "1-3_Referral", "4+_Referral"],
    )

    df["Internet_Type_Clean"] = df["Internet Type"].fillna("No Internet Service")
    df["Offer_Clean"] = df["Offer"].fillna("No Offer")

    df["Population_Density"] = pd.cut(
        df["Population"],
        bins=[-1, 10000, 50000, 1_000_000],
        labels=["Low density (<10K)", "Medium density (10K-50K)", "High density (50K+)"],
    )

    top5_reasons = df["Churn Reason"].value_counts().head(5).index.tolist()
    df["Churn_Reason_Clean"] = df["Churn Reason"].where(
        df["Churn Reason"].isin(top5_reasons), other=None
    )

    return df


def churn_rate_by(df, col, order=None):
    """Return churn rate (%) grouped by col, rounded like the PBI visuals."""
    g = (
        df.groupby(col, observed=True)["Is_Churned"]
        .apply(lambda s: round(100 * s.sum() / len(s), 0) if len(s) else 0)
        .reset_index(name="Churn_Rate")
    )
    if order is not None:
        g[col] = pd.Categorical(g[col], categories=order, ordered=True)
        g = g.sort_values(col)
    else:
        g = g.sort_values("Churn_Rate", ascending=False)
    return g
