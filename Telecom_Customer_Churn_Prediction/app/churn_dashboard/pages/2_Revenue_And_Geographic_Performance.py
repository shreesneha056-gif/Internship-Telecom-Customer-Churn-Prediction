import streamlit as st
import plotly.graph_objects as go

import data as colors
from data_loader import load_data, churn_rate_by, density_churn_pie, REFERRAL_ORDER, OFFER_ORDER
from style import inject_css, page_title, kpi_card, chart_card_open, chart_card_close, slicer_open, slicer_close

st.set_page_config(page_title="Revenue And Geographic Performance", layout="wide", page_icon="🌍")
inject_css()

df = load_data()

OFFER_OPTIONS = OFFER_ORDER
CITY_OPTIONS = ["All"] + sorted(df["City"].dropna().unique().tolist())

with st.sidebar:
    st.markdown("### 🔴 Clear_All_Slicers")
    if st.button("Clear_All_Slicers", use_container_width=True):
        st.session_state["city_filter"] = "All"
        st.session_state["payment_offer_filter"] = OFFER_OPTIONS

    slicer_open("City")
    city_filter = st.selectbox("City", CITY_OPTIONS, index=0, label_visibility="collapsed", key="city_filter")
    slicer_close()

    slicer_open("Payment_Method")
    payment_offer_filter = st.multiselect(
        "Payment_Method", OFFER_OPTIONS, default=OFFER_OPTIONS,
        label_visibility="collapsed", key="payment_offer_filter",
    )
    slicer_close()

# ------------------------------------------------------------------
# Apply every active slicer once, so every chart reflects the same
# filtered population (real cross-filtering)
# ------------------------------------------------------------------
fdf = df[df["Offer"].isin(payment_offer_filter or OFFER_OPTIONS)]
if city_filter != "All":
    fdf = fdf[fdf["City"] == city_filter]

page_title("Revenue_And_Geographic_Performance")

# ------------------------------------------------------------------
# KPI row
# ------------------------------------------------------------------
total_revenue = fdf["Total Revenue"].sum()
total_customers = len(fdf)
avg_cltv = (total_revenue / total_customers) if total_customers else 0
revenue_by_offer = fdf.loc[fdf["Offer"] != "No Offer", "Total Revenue"].sum()

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total_Revenue", f"{total_revenue/1_000_000:.2f}M", rose_label=True)
with k2:
    kpi_card("Total_Customers", f"{total_customers/1000:.0f}K" if total_customers >= 1000 else str(total_customers))
with k3:
    kpi_card("Average_CLTV_In_Per", f"{avg_cltv/1000:.2f}K", rose_label=True)
with k4:
    kpi_card("Revenue_By_Offer", f"{revenue_by_offer/1_000_000:.2f}M", rose_value=True)

# ------------------------------------------------------------------
# Row 2: Churn by city (real lat/lon map) | Churn by referrals (bar)
# ------------------------------------------------------------------
c1, c2 = st.columns(2)
with c1:
    chart_card_open("Churn_Rate_By_City")
    city_agg = (
        fdf.dropna(subset=["Latitude", "Longitude"])
        .groupby("City")
        .agg(lat=("Latitude", "mean"), lon=("Longitude", "mean"),
             total=("churned", "count"), churned=("churned", "sum"))
    )
    if not city_agg.empty:
        city_agg["churn_rate"] = (city_agg["churned"] / city_agg["total"] * 100).round(1)
        city_agg["churn_band"] = city_agg["churn_rate"].apply(colors.churn_band)
        max_total = city_agg["total"].max()

        fig = go.Figure()
        for band in colors.CHURN_BAND_ORDER:
            band_df = city_agg[city_agg["churn_band"] == band]
            if band_df.empty:
                continue
            fig.add_trace(
                go.Scattergeo(
                    lat=band_df["lat"], lon=band_df["lon"],
                    text=[f"{c}: {r}% churn ({t} customers)" for c, r, t in
                          zip(band_df.index, band_df["churn_rate"], band_df["total"])],
                    marker=dict(
                        size=(band_df["total"] / max_total * 40 + 4),
                        color=colors.CHURN_BAND_COLORS[band],
                        opacity=0.8, line=dict(width=0),
                    ),
                    name=band,
                    hoverinfo="text",
                )
            )
        fig.update_geos(
            projection_type="natural earth",
            showland=True, landcolor="#1A1A1A",
            showocean=True, oceancolor=colors.BG,
            showcountries=True, countrycolor="#555555",
            showcoastlines=False, showframe=False, showlakes=False,
            lataxis_showgrid=False, lonaxis_showgrid=False,
            bgcolor=colors.BG,
            fitbounds="locations",
        )
        fig.update_layout(
            paper_bgcolor=colors.BG, height=340, margin=dict(l=0, r=0, t=10, b=0),
            geo=dict(bgcolor=colors.BG),
            legend=dict(
                title="Churn Risk", orientation="h", yanchor="bottom", y=-0.15,
                xanchor="center", x=0.5, font=dict(color=colors.WHITE),
            ),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No customers match the current filters.")
    st.caption(
        "Built from each customer's real ZIP-code latitude/longitude — this dataset covers "
        "California cities only. Bubble size = customer count, color = churn-risk band "
        "(Low <15%, Medium 15-30%, High 30%+), matching the Power BI rule-based conditional formatting."
    )
    chart_card_close()

with c2:
    chart_card_open("Churn_Rate_By_Number_Of_Referrals")
    rrates = churn_rate_by(fdf, "referral_band", order=REFERRAL_ORDER)
    ref_colors = [colors.ROSE if i % 2 == 0 else colors.PALE for i in range(len(rrates))]
    fig = go.Figure(go.Bar(y=rrates.index, x=rrates.values, orientation="h", marker_color=ref_colors, text=rrates.values, textposition="outside"))
    fig.update_layout(
        template=colors.PLOTLY_TEMPLATE, paper_bgcolor=colors.BG, plot_bgcolor=colors.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Churn_Rate", yaxis_title="Referral_Band", yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

# ------------------------------------------------------------------
# Row 3: Churn by offer (bar) | Churn by population density (pie)
# ------------------------------------------------------------------
c3, c4 = st.columns(2)
with c3:
    chart_card_open("Churn_Rate_By_Offer")
    orates = churn_rate_by(fdf, "Offer", order=OFFER_ORDER)
    offer_colors = [colors.ROSE if i % 2 == 0 else colors.PALE for i in range(len(orates))]
    fig = go.Figure(go.Bar(x=orates.index, y=orates.values, marker_color=offer_colors, text=orates.values, textposition="outside"))
    fig.update_layout(
        template=colors.PLOTLY_TEMPLATE, paper_bgcolor=colors.BG, plot_bgcolor=colors.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Offer", yaxis_title="Churn_Rate",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

with c4:
    chart_card_open("Churn_Rate_By_Population_Density")
    dens_pct = density_churn_pie(fdf)
    fig = go.Figure(
        go.Pie(
            labels=dens_pct.index, values=dens_pct.values,
            marker=dict(colors=colors.POP_DENSITY_COLORS), textinfo="percent", sort=False,
        )
    )
    fig.update_layout(
        template=colors.PLOTLY_TEMPLATE, paper_bgcolor=colors.BG, plot_bgcolor=colors.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="v", title="Population_Density"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

st.caption(
    "Computed live from the real Telco customer dataset. City and Payment_Method (Offer) "
    "filters both apply to every chart and KPI on this page."
)
