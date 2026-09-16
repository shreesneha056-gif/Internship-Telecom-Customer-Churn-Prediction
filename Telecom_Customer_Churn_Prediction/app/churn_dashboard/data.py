"""
Shared data + style constants for the Streamlit rebuild of the
"Churn & Retention / Revenue & Geographic Performance" Power BI dashboard.

Values below are taken directly from the published Power BI report
(dashboard.pdf export).
"""

import pandas as pd

# ---------------------------------------------------------------
# THEME — colors sampled directly from the PDF export
# ---------------------------------------------------------------
BG = "#333333"           # canvas + card background (charcoal)
CARD_BORDER = "#5A5A5A"
BLACK = "#000000"        # title bar / slicer header background
ROSE = "#DE6A73"         # primary accent (bars, KPI highlight)
PALE = "#E8E6E0"         # secondary/alternating bar color (near-white)
GREY_TEXT = "#B5B5B5"
WHITE = "#FFFFFF"
MAROON = "#77494C"       # area chart fill (odd bands)
GREY_FILL = "#848484"    # area chart fill (even bands)

DONUT_COLORS = ["#73361C", "#A8542E", "#DE6A73", "#F0A787", "#F7D9C4"]

PLOTLY_TEMPLATE = "plotly_dark"

# ---------------------------------------------------------------
# PAGE 1 — Churn_And_Retention_Overview
# ---------------------------------------------------------------
KPI_CHURN = {
    "Total_Customers": "7K",
    "Churn_Rate_In_Per": "26.54",
    "Avg_Tenure_In_Per": "32.39",
    "Churned_Customers": "2K",
}

churn_by_contract = pd.DataFrame(
    {
        "Contract": ["Month-to-Month", "One Year", "Two Year"],
        "Churn_Rate": [46, 11, 3],
        "color": [ROSE, PALE, ROSE],
    }
)

churn_reason = pd.DataFrame(
    {
        "CHURN_REASON_CLEAN": [
            "Competitor had better devices",
            "Competitor made better offer",
            "Attitude of support person",
            "Don't know",
            "Competitor offered more data",
        ],
        "pct": [28.69, 28.51, 20.16, 11.92, 10.72],
    }
)

churn_by_tenure = pd.DataFrame(
    {
        "Tenure_Band": ["0-12 months", "12-24 months", "24-48 months", "48+ months"],
        "Churn_Rate": [48, 30, 21, 10],
        "color": [MAROON, GREY_FILL, MAROON, GREY_FILL],
    }
)

churn_by_internet = pd.DataFrame(
    {
        "Internet_Type": ["Fiber Optic", "Cable", "DSL", "No Internet Service"],
        "Churn_Rate": [41, 26, 19, 7],
        "color": [ROSE, PALE, ROSE, PALE],
    }
)

CONTRACT_OPTIONS = ["Month-to-Month", "One Year", "Two Year"]
INTERNET_SERVICE_OPTIONS = ["False", "True"]
PAYMENT_METHOD_OPTIONS = ["Bank Withdrawal", "Credit Card", "Mailed Check"]

# ---------------------------------------------------------------
# PAGE 2 — Revenue_And_Geographic_Performance
# ---------------------------------------------------------------
KPI_REVENUE = {
    "Total_Revenue": "21.37M",
    "Total_Customers": "7K",
    "Average_CLTV_In_Per": "3.03K",
    "Revenue_By_Offer": "10.02M",
}

churn_by_referrals = pd.DataFrame(
    {
        "Referral_Band": ["1-3_Referral", "0_Referral", "4+_Referral"],
        "Churn_Rate": [36, 33, 4],
        "color": [ROSE, PALE, ROSE],
    }
)

churn_by_offer = pd.DataFrame(
    {
        "Offer": ["Offer E", "No Offer", "Offer D", "Offer C", "Offer B", "Offer A"],
        "Churn_Rate": [53, 27, 27, 23, 12, 7],
        "color": [ROSE, PALE, ROSE, PALE, ROSE, PALE],
    }
)

population_density = pd.DataFrame(
    {
        "Population_Density": ["High density (50K+)", "Medium density (10K-50K)", "Low density (<10K)"],
        "pct": [36.79, 33.52, 29.69],
    }
)
POP_DENSITY_COLORS = [WHITE, ROSE, "#F0A7B0"]

# Illustrative city bubble locations (visual parity only — the source map
# has no printed per-city values in the export, so exact figures aren't
# available; bubble positions/sizes approximate the clusters visible in the
# PDF's world map: heavy concentration over the southern/central US,
# a medium cluster over Northern Europe, and light scattered blobs over
# Canada, the Middle East, West Africa, South America, and Australia).
city_bubbles = pd.DataFrame(
    {
        "city": [
            "Southern/Central US (large cluster)", "Central US (secondary cluster)",
            "Canada", "Northern Europe", "Middle East", "West Africa",
            "South America (Brazil)", "Australia (east)", "Australia (southeast)", "New Zealand",
        ],
        "lat": [32, 36, 60, 55, 28, 8, -15, -28, -33, -37],
        "lon": [-97, -90, -100, 12, 50, 5, -55, 135, 146, 172],
        "size": [70, 50, 16, 36, 16, 13, 22, 26, 16, 11],
    }
)

CITY_OPTIONS = ["All"]
PAYMENT_METHOD_OFFER_OPTIONS = ["No Offer", "Offer A", "Offer B", "Offer C", "Offer D", "Offer E"]
