"""
Shared helpers for the Churn & Retention / Revenue & Geographic Streamlit app.
Data prep here mirrors the original Power BI model 1:1:
  - Tenure_Band, Referral_Band, Population_Density are the exact DAX
    calculated columns from the .pbix (verified against PowerBI-Ray extract).
  - Churn_Rate, Avg_Tenure, Total_Revenue, Avg_CLTV, Revenue_By_Offer are the
    exact DAX measures from the .pbix `_Measurements` table.
"""

import os
import pandas as pd
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# ---------------------------------------------------------------------------
# Colors extracted directly from the .pbix report (dataPoint fill overrides)
# ---------------------------------------------------------------------------
BG_COLOR = "#0e0e0e"          # page / app background
PANEL_BG = "#171717"          # card / chart panel background
PANEL_BORDER = "#2a2a2a"
ACCENT = "#DE6A73"            # primary rose accent (literal color found in .pbix)
SECONDARY = "#FFFFFF"         # alternating secondary bar color
TEXT_MAIN = "#F2F2F2"
TEXT_MUTED = "#B3B3B3"

DONUT_PALETTE = ["#7A3A35", "#B25046", "#DE6A73", "#EDA394", "#F6D9CE"]
DENSITY_PALETTE = {
    "High density (50K+)": "#FFFFFF",
    "Medium density (10K-50K)": "#DE6A73",
    "Low density (<10K)": "#F0B8BE",
}


def alt_colors(n: int) -> list:
    """Alternating accent/secondary colors by rank position, exactly like the
    conditional dataPoint overrides in the source .pbix bar/column/area charts."""
    return [ACCENT if i % 2 == 0 else SECONDARY for i in range(n)]


@st.cache_data
def load_data() -> pd.DataFrame:
    acc = pd.read_csv(os.path.join(DATA_DIR, "customer_account_status.csv"))
    demo = pd.read_csv(os.path.join(DATA_DIR, "customer_demographics.csv"))
    loc = pd.read_csv(os.path.join(DATA_DIR, "customer_location.csv"))
    serv = pd.read_csv(os.path.join(DATA_DIR, "customer_services.csv"))
    pop = pd.read_csv(os.path.join(DATA_DIR, "zipcode_population.csv"))

    df = (
        acc.merge(demo, on="Customer ID", how="left")
        .merge(loc, on="Customer ID", how="left")
        .merge(serv, on="Customer ID", how="left")
        .merge(pop, on="Zip Code", how="left")
    )

    # --- DAX calculated column: Tenure_Band ---
    def tenure_band(t):
        if t < 12:
            return "0-12 months"
        elif t < 24:
            return "12-24 months"
        elif t < 48:
            return "24-48 months"
        return "48+ months"

    df["Tenure_Band"] = df["Tenure in Months"].apply(tenure_band)

    # --- DAX calculated column: Referral_Band ---
    def referral_band(n):
        if n <= 0:
            return "0_Referral"
        elif n <= 3:
            return "1-3_Referral"
        return "4+_Referral"

    df["Referral_Band"] = df["Number of Referrals"].apply(referral_band)

    # --- DAX calculated column: Population_Density ---
    def density(p):
        if pd.isna(p):
            return None
        if p < 10000:
            return "Low density (<10K)"
        elif p < 50000:
            return "Medium density (10K-50K)"
        return "High density (50K+)"

    df["Population_Density"] = df["Population"].apply(density)

    # Offer / churn reason "clean" fields (blank -> No Offer)
    df["Offer_Clean"] = df["Offer"].fillna("No Offer")
    df["Is_Churned"] = df["Customer Status"] == "Churned"

    return df


def kpi_card(label: str, value: str, value_color: str = SECONDARY):
    st.markdown(
        f"""
        <div style="background-color:{PANEL_BG};border:1px solid {PANEL_BORDER};
                    border-radius:6px;padding:14px 18px;height:100%;">
            <div style="color:{value_color};font-size:13px;font-weight:500;
                        margin-bottom:6px;">{label}</div>
            <div style="color:{TEXT_MAIN};font-size:30px;font-weight:600;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def panel_start(title: str):
    st.markdown(
        f"""
        <div style="background-color:{PANEL_BG};border:1px solid {PANEL_BORDER};
                    border-radius:6px;padding:14px 18px 4px 18px;">
            <div style="color:{TEXT_MAIN};font-size:15px;font-weight:600;
                        margin-bottom:6px;">{title}</div>
        """,
        unsafe_allow_html=True,
    )


def panel_end():
    st.markdown("</div>", unsafe_allow_html=True)


def base_layout(fig, height=340):
    """Apply the shared dark-theme layout to every plotly figure."""
    fig.update_layout(
        paper_bgcolor=PANEL_BG,
        plot_bgcolor=PANEL_BG,
        font_color=TEXT_MAIN,
        margin=dict(l=10, r=10, t=10, b=10),
        height=height,
        showlegend=False,
    )
    fig.update_xaxes(gridcolor=PANEL_BORDER, zerolinecolor=PANEL_BORDER, color=TEXT_MUTED)
    fig.update_yaxes(gridcolor=PANEL_BORDER, zerolinecolor=PANEL_BORDER, color=TEXT_MUTED)
    return fig


def format_k(x):
    return f"{x/1000:.0f}K"


def format_k2(x):
    return f"{x/1000:.2f}K"


def format_m2(x):
    return f"{x/1_000_000:.2f}M"


def churn_rate(sub: pd.DataFrame) -> float:
    total = len(sub)
    if total == 0:
        return 0.0
    return round(sub["Is_Churned"].sum() / total * 100, 0)
