"""Chart builders that need more than a one-liner go here, so the page
scripts stay readable."""

import numpy as np
from scipy.interpolate import CubicSpline
import plotly.graph_objects as go


def banded_area_chart(labels, values, fill_colors, line_colors, bg, white, height=340):
    """
    Smooth curved area chart where the fill color (and line color) changes
    per category band, matching the source Power BI visual: a single
    continuous smooth curve through the category values, with the area
    under each category's own x-span shaded a different color, and value
    labels above each point.
    """
    n = len(labels)
    x_anchor = np.arange(n)
    y_anchor = np.array(values, dtype=float)

    cs = CubicSpline(x_anchor, y_anchor)
    xs_fine = np.linspace(0, n - 1, 400)
    ys_fine = cs(xs_fine)
    ys_fine = np.clip(ys_fine, 0, None)  # a spline can dip slightly below 0 between points; clamp for a churn-rate axis

    # Band boundaries: half a unit either side of each anchor, so each
    # category "owns" the fill directly under its own tick, same as the source.
    boundaries = [x_anchor[0] - 0.5] + [
        (x_anchor[i] + x_anchor[i + 1]) / 2 for i in range(n - 1)
    ] + [x_anchor[-1] + 0.5]

    fig = go.Figure()
    for i in range(n):
        lo, hi = boundaries[i], boundaries[i + 1]
        mask = (xs_fine >= lo) & (xs_fine <= hi)
        seg_x = xs_fine[mask]
        seg_y = ys_fine[mask]
        if len(seg_x) < 2:
            continue
        fig.add_trace(
            go.Scatter(
                x=seg_x, y=seg_y, mode="lines",
                line=dict(color=line_colors[i % len(line_colors)], width=2.5, shape="spline"),
                fill="tozeroy", fillcolor=fill_colors[i % len(fill_colors)],
                showlegend=False, hoverinfo="skip",
            )
        )

    fig.add_trace(
        go.Scatter(
            x=x_anchor, y=y_anchor, mode="markers+text",
            marker=dict(color=white, size=6),
            text=[str(int(round(v))) for v in y_anchor], textposition="top center",
            textfont=dict(color=white),
            showlegend=False, hoverinfo="skip",
        )
    )

    fig.update_layout(
        paper_bgcolor=bg, plot_bgcolor=bg, height=height,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(
            tickmode="array", tickvals=list(x_anchor), ticktext=list(labels),
            range=[boundaries[0], boundaries[-1]], title="Tenure_Band",
        ),
        yaxis=dict(title="Churn_Rate", rangemode="tozero"),
    )
    return fig
