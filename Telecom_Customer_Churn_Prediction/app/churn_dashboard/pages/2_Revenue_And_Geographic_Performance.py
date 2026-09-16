import streamlit as st
import plotly.graph_objects as go

import data as d
from style import inject_css, page_title, kpi_card, chart_card_open, chart_card_close, slicer_open, slicer_close

st.set_page_config(page_title="Revenue And Geographic Performance", layout="wide", page_icon="🌍")
inject_css()

with st.sidebar:
    st.markdown("### 🔴 Clear_All_Slicers")
    if st.button("Clear_All_Slicers", use_container_width=True):
        st.session_state["city_filter"] = "All"
        st.session_state["payment_offer_filter"] = d.PAYMENT_METHOD_OFFER_OPTIONS

    slicer_open("City")
    city_filter = st.selectbox("City", d.CITY_OPTIONS, index=0, label_visibility="collapsed", key="city_filter")
    slicer_close()

    slicer_open("Payment_Method")
    payment_offer_filter = st.multiselect(
        "Payment_Method", d.PAYMENT_METHOD_OFFER_OPTIONS, default=d.PAYMENT_METHOD_OFFER_OPTIONS,
        label_visibility="collapsed", key="payment_offer_filter",
    )
    slicer_close()

page_title("Revenue_And_Geographic_Performance")

# ------------------------------------------------------------------
# KPI row
# ------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total_Revenue", d.KPI_REVENUE["Total_Revenue"], rose_label=True, rose_value=False)
with k2:
    kpi_card("Total_Customers", d.KPI_REVENUE["Total_Customers"], rose_label=False, rose_value=False)
with k3:
    kpi_card("Average_CLTV_In_Per", d.KPI_REVENUE["Average_CLTV_In_Per"], rose_label=True, rose_value=False)
with k4:
    kpi_card("Revenue_By_Offer", d.KPI_REVENUE["Revenue_By_Offer"], rose_label=False, rose_value=True)

# ------------------------------------------------------------------
# Row 2: Churn by city (map) | Churn by number of referrals (bar)
# ------------------------------------------------------------------
c1, c2 = st.columns(2)
with c1:
    chart_card_open("Churn_Rate_By_City")
    fig = go.Figure(
        go.Scattergeo(
            lat=d.city_bubbles["lat"], lon=d.city_bubbles["lon"],
            text=d.city_bubbles["city"],
            marker=dict(
                size=d.city_bubbles["size"], color=d.ROSE, opacity=0.55,
                line=dict(width=0), sizemode="diameter",
            ),
            hoverinfo="text",
        )
    )
    fig.update_geos(
        projection_type="natural earth",
        showland=True, landcolor="#1A1A1A",
        showocean=True, oceancolor=d.BG,
        showcountries=True, countrycolor="#555555",
        showcoastlines=False, showframe=False,
        showlakes=False, lataxis_showgrid=False, lonaxis_showgrid=False,
        bgcolor=d.BG,
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=340, margin=dict(l=0, r=0, t=10, b=0),
        geo=dict(bgcolor=d.BG),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.caption("Illustrative reproduction — the source map has no printed per-city values in the export.")
    chart_card_close()

with c2:
    chart_card_open("Churn_Rate_By_Number_Of_Referrals")
    fig = go.Figure(
        go.Bar(
            y=d.churn_by_referrals["Referral_Band"], x=d.churn_by_referrals["Churn_Rate"], orientation="h",
            marker_color=d.churn_by_referrals["color"],
            text=d.churn_by_referrals["Churn_Rate"], textposition="outside",
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=320, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Churn_Rate", yaxis_title="Referral_Band",
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

# ------------------------------------------------------------------
# Row 3: Churn by offer (bar) | Churn by population density (pie)
# ------------------------------------------------------------------
c3, c4 = st.columns(2)
offer_label_map = {
    "No Offer": "No Offer", "Offer A": "Offer A", "Offer B": "Offer B",
    "Offer C": "Offer C", "Offer D": "Offer D", "Offer E": "Offer E",
}
offer_df = d.churn_by_offer[d.churn_by_offer["Offer"].isin(payment_offer_filter)] \
    if payment_offer_filter else d.churn_by_offer

with c3:
    chart_card_open("Churn_Rate_By_Offer")
    fig = go.Figure(
        go.Bar(
            x=offer_df["Offer"], y=offer_df["Churn_Rate"],
            marker_color=offer_df["color"],
            text=offer_df["Churn_Rate"], textposition="outside",
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Offer", yaxis_title="Churn_Rate",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

with c4:
    chart_card_open("Churn_Rate_By_Population_Density")
    fig = go.Figure(
        go.Pie(
            labels=d.population_density["Population_Density"], values=d.population_density["pct"],
            marker=dict(colors=d.POP_DENSITY_COLORS),
            textinfo="percent", sort=False,
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="v", title="Population_Density"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

st.caption(
    "Rebuilt from the exported Power BI report. Payment_Method filter is live against "
    "the Churn_Rate_By_Offer chart; City has only a single 'All' value in the source export."
)
