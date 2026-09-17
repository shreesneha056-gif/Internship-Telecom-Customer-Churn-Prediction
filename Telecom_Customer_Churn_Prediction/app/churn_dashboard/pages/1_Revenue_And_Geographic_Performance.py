import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils import (
    load_data, kpi_card, panel_start, panel_end, base_layout, alt_colors,
    DENSITY_PALETTE, ACCENT, SECONDARY, TEXT_MAIN, TEXT_MUTED, BG_COLOR,
    PANEL_BG, PANEL_BORDER, format_m2, format_k, format_k2,
)

st.set_page_config(
    page_title="Revenue And Geographic Performance",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
        .stApp {{ background-color: {BG_COLOR}; }}
        section[data-testid="stSidebar"] {{ background-color: {PANEL_BG};
            border-right: 1px solid {PANEL_BORDER}; }}
        .title-bar {{
            background-color: #000000; color: #FFFFFF; text-align:center;
            padding: 14px 0; font-size: 26px; font-weight: 600;
            border-radius: 4px; margin-bottom: 14px; letter-spacing: 0.5px;
        }}
        h1, h2, h3, p, span, label, div {{ color: {TEXT_MAIN}; }}
        .stMultiSelect [data-baseweb="tag"] {{ background-color: {ACCENT}; }}
    </style>
    """,
    unsafe_allow_html=True,
)

df = load_data()

# ---------------------------------------------------------------------------
# Sidebar - slicers (City, Payment_Method / Offer)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧹 Clear_All_Slicers")
    if st.button("Clear All Slicers", use_container_width=True):
        for k in ["city_f", "offer_f"]:
            st.session_state.pop(k, None)
        st.rerun()

    st.markdown("#### City")
    city_opts = ["All"] + sorted(df["City"].dropna().unique().tolist())
    city_f = st.selectbox("City", city_opts, index=0, key="city_f", label_visibility="collapsed")

    st.markdown("#### Payment_Method (Offer)")
    offer_opts = ["No Offer", "Offer A", "Offer B", "Offer C", "Offer D", "Offer E"]
    offer_f = st.multiselect("Offer", offer_opts, default=[], key="offer_f",
                              label_visibility="collapsed")

# ---------------------------------------------------------------------------
# Apply filters
# ---------------------------------------------------------------------------
fdf = df.copy()
if city_f != "All":
    fdf = fdf[fdf["City"] == city_f]
if offer_f:
    fdf = fdf[fdf["Offer_Clean"].isin(offer_f)]

st.markdown('<div class="title-bar">Revenue_And_Geographic_Performance</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
total_customers = fdf["Customer ID"].nunique()
total_revenue = fdf["Total Revenue"].sum()
avg_cltv = fdf["Total Revenue"].mean() if total_customers else 0
revenue_by_offer = fdf.loc[fdf["Offer"].notna(), "Total Revenue"].sum()

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total_Revenue", format_m2(total_revenue), ACCENT)
with k2:
    kpi_card("Total_Customers", format_k(total_customers), SECONDARY)
with k3:
    kpi_card("Average_CLTV_In_Per", format_k2(avg_cltv), SECONDARY)
with k4:
    kpi_card("Revenue_By_Offer", format_m2(revenue_by_offer), ACCENT)

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Row 1: Churn_Rate_By_City (map) | Churn_Rate_By_Number_Of_Referrals
# ---------------------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    panel_start("Churn_Rate_By_City")
    city_g = (
        fdf.groupby(["City", "Latitude", "Longitude"])
        .agg(Total=("Customer ID", "nunique"), Churned=("Is_Churned", "sum"))
        .reset_index()
    )
    city_g["Churn_Rate"] = (city_g["Churned"] / city_g["Total"] * 100).round(1)
    if len(city_g):
        # Plain go.Scattergeo: no Mapbox token, no external tile server,
        # and no dependency on px.scatter_mapbox internals that vary across
        # plotly/pandas versions - safest option for Streamlit Cloud.
        fig = go.Figure(
            go.Scattergeo(
                lat=city_g["Latitude"], lon=city_g["Longitude"],
                text=city_g["City"] + "<br>Churn Rate: " + city_g["Churn_Rate"].astype(str) + "%",
                hoverinfo="text",
                marker=dict(
                    size=(city_g["Churn_Rate"] / city_g["Churn_Rate"].max() * 22 + 6),
                    color=city_g["Churn_Rate"],
                    colorscale=[[0, "#F6D9CE"], [0.5, ACCENT], [1, "#7A3A35"]],
                    line=dict(width=0.5, color="#000000"),
                    showscale=False,
                ),
            )
        )
        fig.update_geos(
            scope="usa",
            projection_type="albers usa",
            bgcolor=PANEL_BG,
            landcolor="#242424",
            lakecolor=PANEL_BG,
            showland=True,
            showcountries=False,
            showsubunits=True,
            subunitcolor="#3a3a3a",
            center=dict(lat=36.7, lon=-119.4),
        )
        st.plotly_chart(base_layout(fig, height=340), use_container_width=True,
                         config={"displayModeBar": False})
    else:
        st.info("No data for current filter selection.")
    panel_end()

with c2:
    panel_start("Churn_Rate_By_Number_Of_Referrals")
    order = ["1-3_Referral", "0_Referral", "4+_Referral"]
    g = (
        fdf.groupby("Referral_Band")["Is_Churned"]
        .mean().mul(100).round(0).reset_index(name="Churn_Rate")
        .sort_values("Churn_Rate", ascending=False)
    )
    fig = go.Figure(
        go.Bar(
            x=g["Churn_Rate"], y=g["Referral_Band"], orientation="h",
            text=g["Churn_Rate"].astype(int), textposition="outside",
            marker_color=alt_colors(len(g)),
        )
    )
    fig.update_layout(yaxis_title="Referral_Band", xaxis_title="Churn_Rate",
                       yaxis=dict(autorange="reversed"))
    st.plotly_chart(base_layout(fig), use_container_width=True, config={"displayModeBar": False})
    panel_end()

# ---------------------------------------------------------------------------
# Row 2: Churn_Rate_By_Offer | Churn_Rate_By_Population_Density
# ---------------------------------------------------------------------------
c3, c4 = st.columns(2)

with c3:
    panel_start("Churn_Rate_By_Offer")
    g = (
        fdf.groupby("Offer_Clean")["Is_Churned"]
        .mean().mul(100).round(0).reset_index(name="Churn_Rate")
        .sort_values("Churn_Rate", ascending=False)
    )
    fig = go.Figure(
        go.Bar(
            x=g["Offer_Clean"], y=g["Churn_Rate"],
            text=g["Churn_Rate"].astype(int), textposition="outside",
            marker_color=alt_colors(len(g)),
        )
    )
    fig.update_layout(yaxis_title="Churn_Rate", xaxis_title="Offer")
    st.plotly_chart(base_layout(fig), use_container_width=True, config={"displayModeBar": False})
    panel_end()

with c4:
    panel_start("Churn_Rate_By_Population_Density")
    g = (
        fdf.dropna(subset=["Population_Density"])
        .groupby("Population_Density")["Is_Churned"]
        .mean().mul(100).reset_index(name="Churn_Rate")
    )
    fig = go.Figure(
        go.Pie(
            labels=g["Population_Density"], values=g["Churn_Rate"], hole=0.0,
            marker=dict(colors=[DENSITY_PALETTE.get(x, SECONDARY) for x in g["Population_Density"]]),
            textinfo="percent", textfont_color="#000000",
        )
    )
    fig.update_layout(showlegend=True, legend=dict(font=dict(color=TEXT_MAIN, size=10)))
    st.plotly_chart(base_layout(fig, height=340), use_container_width=True, config={"displayModeBar": False})
    panel_end()
