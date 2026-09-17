"""Shared theme colors, sampled directly from the PDF export."""

BG = "#333333"           # canvas + card background (charcoal)
CARD_BORDER = "#5A5A5A"
BLACK = "#000000"        # title bar / slicer header background
ROSE = "#DE6A73"         # primary accent (bars, KPI highlight)
PALE = "#E8E6E0"         # secondary/alternating bar color (near-white)
GREY_TEXT = "#B5B5B5"
WHITE = "#FFFFFF"
MAROON = "#77494C"       # area/bar fill (odd tenure bands)
GREY_FILL = "#848484"    # area/bar fill (even tenure bands)

DONUT_COLORS = ["#73361C", "#A8542E", "#DE6A73", "#F0A787", "#F7D9C4"]
POP_DENSITY_COLORS = [WHITE, ROSE, "#F0A7B0"]

# Churn-risk bands for the city map, matching the Power BI "Rules" conditional
# formatting (Format style: Rules) set on the Churn_Rate_By_City bubble map:
#   Low    : churn_rate <  15%  -> green
#   Medium : 15% <= churn_rate < 30%  -> amber
#   High   : churn_rate >= 30%  -> red/rose
CHURN_BAND_ORDER = ["Low (<15%)", "Medium (15-30%)", "High (30%+)"]
CHURN_BAND_COLORS = {
    "Low (<15%)": "#4CAF50",
    "Medium (15-30%)": "#FFC107",
    "High (30%+)": ROSE,
}


def churn_band(rate):
    """Bucket a churn-rate percentage into the same 3 tiers used by the
    Power BI rule-based conditional formatting."""
    if rate < 15:
        return "Low (<15%)"
    elif rate < 30:
        return "Medium (15-30%)"
    return "High (30%+)"

PLOTLY_TEMPLATE = "plotly_dark"


def alternating(n, start_with=ROSE, alt=PALE):
    return [start_with if i % 2 == 0 else alt for i in range(n)]


def alternating_tenure(n):
    return [MAROON if i % 2 == 0 else GREY_FILL for i in range(n)]
