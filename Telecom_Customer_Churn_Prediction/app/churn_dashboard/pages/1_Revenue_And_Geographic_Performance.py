import streamlit as st
import plotly.graph_objects as go
from utils import (
    load_data, inject_css, kpi_card, chart_title, page_title, churn_rate_by,
    PLOTLY_LAYOUT, ROSE, WHITE_BAR, DENSITY_COLORS,
)

st.set_page_config(page_title="Revenue And Geographic Performance", layout="wide", page_icon="🌍")
inject_css()

df = load_data()

# ----------------------------- SIDEBAR SLICERS -----------------------------
with st.sidebar:
    if st.button("🔴  Clear All Slicers", use_container_width=True):
        for k in ["city_f", "offer_f"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

    st.markdown("**City**")
    city_opts = ["All"] + sorted(df["City"].dropna().unique().tolist())
    city_f = st.selectbox("City", city_opts, key="city_f", label_visibility="collapsed")

    st.markdown("**Payment_Method**")
    offer_opts = ["No Offer", "Offer A", "Offer B", "Offer C", "Offer D", "Offer E"]
    offer_f = st.multiselect("Payment_Method", offer_opts, default=offer_opts,
                              key="offer_f", label_visibility="collapsed")

# ----------------------------- FILTER DATA -----------------------------
fdf = df[df["Offer_Clean"].isin(offer_f)]
if city_f != "All":
    fdf = fdf[fdf["City"] == city_f]

# ----------------------------- TITLE -----------------------------
page_title("Revenue_And_Geographic_Performance")

# ----------------------------- KPI ROW -----------------------------
total_revenue = fdf["Total Revenue"].sum()
total_customers = len(fdf)
avg_cltv = fdf["Total Revenue"].mean() if total_customers else 0
revenue_by_offer = fdf.loc[fdf["Offer"].notna(), "Total Revenue"].sum()

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Total_Revenue", f"{total_revenue/1_000_000:.2f}M")
with c2:
    kpi_card("Total_Customers", f"{total_customers/1000:.0f}K" if total_customers >= 1000 else total_customers)
with c3:
    kpi_card("Average_CLTV_In_Per", f"{avg_cltv/1000:.2f}K")
with c4:
    kpi_card("Revenue_By_Offer", f"{revenue_by_offer/1_000_000:.2f}M")

st.write("")

# ----------------------------- ROW 1: City map | Referrals -----------------------------
row1_left, row1_right = st.columns(2)

with row1_left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_title("Churn_Rate_By_City")
    city_agg = fdf.groupby("City", observed=True).agg(
        Customers=("Customer ID", "count"),
        Lat=("Latitude", "mean"),
        Lon=("Longitude", "mean"),
        Churned=("Is_Churned", "sum"),
    ).reset_index()
    if len(city_agg):
        fig = go.Figure(go.Scattergeo(
            lat=city_agg["Lat"], lon=city_agg["Lon"],
            text=city_agg["City"] + "<br>Customers: " + city_agg["Customers"].astype(str),
            marker=dict(
                size=city_agg["Customers"].clip(upper=200) ** 0.5 * 3,
                color=ROSE, opacity=0.6, line=dict(width=0),
            ),
        ))
        fig.update_geos(
            projection_type="natural earth", bgcolor="#1a1a1f",
            showland=True, landcolor="#2b2b31", showocean=True, oceancolor="#141418",
            showcountries=True, countrycolor="#3a3a42", showcoastlines=False,
            lataxis_range=[10, 60], lonaxis_range=[-130, -60],
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=340, geo=dict(bgcolor="#1a1a1f"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No data for current filter selection.")
    st.markdown('</div>', unsafe_allow_html=True)

with row1_right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_title("Churn_Rate_By_Number_Of_Referrals")
    order = ["1-3_Referral", "0_Referral", "4+_Referral"]
    g = churn_rate_by(fdf, "Referral_Band", order=None)
    g["Referral_Band"] = g["Referral_Band"].astype(str)
    g = g.set_index("Referral_Band").reindex(order).reset_index()
    bar_colors = [ROSE, WHITE_BAR, ROSE]
    fig = go.Figure(go.Bar(
        x=g["Churn_Rate"], y=g["Referral_Band"], orientation="h",
        marker_color=bar_colors, text=g["Churn_Rate"], textposition="outside",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=340,
                       xaxis_title="Churn_Rate", yaxis_title="Referral_Band",
                       yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- ROW 2: Offer | Population Density -----------------------------
row2_left, row2_right = st.columns(2)

with row2_left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_title("Churn_Rate_By_Offer")
    order = ["Offer E", "No Offer", "Offer D", "Offer C", "Offer B", "Offer A"]
    g = churn_rate_by(fdf, "Offer_Clean", order=None).set_index("Offer_Clean").reindex(order).reset_index()
    bar_colors = [ROSE, WHITE_BAR, ROSE, WHITE_BAR, ROSE, WHITE_BAR]
    fig = go.Figure(go.Bar(
        x=g["Offer_Clean"], y=g["Churn_Rate"], marker_color=bar_colors,
        text=g["Churn_Rate"], textposition="outside",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=320, yaxis_title="Churn_Rate", xaxis_title="Offer")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with row2_right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_title("Churn_Rate_By_Population_Density")
    order = ["High density (50K+)", "Medium density (10K-50K)", "Low density (<10K)"]
    g = churn_rate_by(fdf, "Population_Density", order=None).set_index("Population_Density").reindex(order).reset_index()
    if g["Churn_Rate"].sum() > 0:
        fig = go.Figure(go.Pie(
            labels=g["Population_Density"], values=g["Churn_Rate"], hole=0,
            marker=dict(colors=DENSITY_COLORS),
            textinfo="percent", textfont=dict(color="black", size=12),
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=320, legend=dict(title="Population_Density"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No data for current filter selection.")
    st.markdown('</div>', unsafe_allow_html=True)
