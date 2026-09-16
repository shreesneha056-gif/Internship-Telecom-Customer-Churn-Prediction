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

PLOTLY_TEMPLATE = "plotly_dark"


def alternating(n, start_with=ROSE, alt=PALE):
    return [start_with if i % 2 == 0 else alt for i in range(n)]


def alternating_tenure(n):
    return [MAROON if i % 2 == 0 else GREY_FILL for i in range(n)]
