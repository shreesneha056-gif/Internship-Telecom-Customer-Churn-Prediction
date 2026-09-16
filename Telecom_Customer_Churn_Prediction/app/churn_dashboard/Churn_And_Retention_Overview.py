import streamlit as st
import plotly.graph_objects as go

import data as colors
from data_loader import load_data, churn_rate_by, top5_churn_reason_pie, TENURE_ORDER, CONTRACT_ORDER
from style import inject_css, page_title, kpi_card, chart_card_open, chart_card_close, slicer_open, slicer_close

st.set_page_config(page_title="Churn And Retention Overview", layout="wide", page_icon="📉")
inject_css()

df = load_data()

CONTRACT_OPTIONS = CONTRACT_ORDER
INTERNET_SERVICE_OPTIONS = ["True", "False"]
PAYMENT_METHOD_OPTIONS = ["Bank Withdrawal", "Credit Card", "Mailed Check"]

# ------------------------------------------------------------------
# Sidebar — slicers (mirrors the Power BI slicer panel, and genuinely
# cross-filters every chart on the page, not just one)
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🔴 Clear_All_Slicers")
    if st.button("Clear_All_Slicers", use_container_width=True):
        st.session_state["contract_filter"] = CONTRACT_OPTIONS
        st.session_state["internet_filter"] = INTERNET_SERVICE_OPTIONS
        st.session_state["payment_filter"] = PAYMENT_METHOD_OPTIONS

    slicer_open("Contract_Type")
    contract_filter = st.multiselect(
        "Contract_Type", CONTRACT_OPTIONS, default=CONTRACT_OPTIONS,
        label_visibility="collapsed", key="contract_filter",
    )
    slicer_close()

    slicer_open("Internet_Service")
    internet_filter = st.multiselect(
        "Internet_Service", INTERNET_SERVICE_OPTIONS, default=INTERNET_SERVICE_OPTIONS,
        label_visibility="collapsed", key="internet_filter",
    )
    slicer_close()

    slicer_open("Payment_Method")
    payment_filter = st.multiselect(
        "Payment_Method", PAYMENT_METHOD_OPTIONS, default=PAYMENT_METHOD_OPTIONS,
        label_visibility="collapsed", key="payment_filter",
    )
    slicer_close()

# ------------------------------------------------------------------
# Apply every active slicer to the underlying data ONCE, so every
# chart below reflects the same filtered population (real cross-filtering)
# ------------------------------------------------------------------
fdf = df[
    df["Contract"].isin(contract_filter or CONTRACT_OPTIONS)
    & df["has_internet"].isin(internet_filter or INTERNET_SERVICE_OPTIONS)
    & df["Payment Method"].isin(payment_filter or PAYMENT_METHOD_OPTIONS)
]

page_title("Churn_And_Retention_Overview")

# ------------------------------------------------------------------
# KPI row
# ------------------------------------------------------------------
total_customers = len(fdf)
churned_customers = int(fdf["churned"].sum())
churn_rate = round(churned_customers / total_customers * 100, 2) if total_customers else 0.0
avg_tenure = round(fdf["Tenure in Months"].mean(), 2) if total_customers else 0.0

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total_Customers", f"{total_customers/1000:.0f}K" if total_customers >= 1000 else str(total_customers), rose_label=True)
with k2:
    kpi_card("Churn_Rate_In_Per", f"{churn_rate:.2f}", rose_value=True)
with k3:
    kpi_card("Avg_Tenure_In_Per", f"{avg_tenure:.2f}", rose_label=True)
with k4:
    kpi_card("Churned_Customers", f"{churned_customers/1000:.0f}K" if churned_customers >= 1000 else str(churned_customers), rose_value=True)

# ------------------------------------------------------------------
# Row 2: Churn by contract (bar) | Top 5 churn reasons (donut)
# ------------------------------------------------------------------
c1, c2 = st.columns(2)
with c1:
    chart_card_open("Churn_Rate_By_Contract")
    rates = churn_rate_by(fdf, "Contract", order=CONTRACT_ORDER)
    bar_colors = [colors.ROSE if i % 2 == 0 else colors.PALE for i in range(len(rates))]
    fig = go.Figure(go.Bar(x=rates.index, y=rates.values, marker_color=bar_colors, text=rates.values, textposition="outside"))
    fig.update_layout(
        template=colors.PLOTLY_TEMPLATE, paper_bgcolor=colors.BG, plot_bgcolor=colors.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Contract", yaxis_title="Churn_Rate",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

with c2:
    chart_card_open("Top_5_Churn_Reason_For_Churn")
    reason_pct = top5_churn_reason_pie(fdf)
    fig = go.Figure(
        go.Pie(
            labels=reason_pct.index, values=reason_pct.values, hole=0.55,
            marker=dict(colors=colors.DONUT_COLORS), textinfo="percent", sort=False,
        )
    )
    fig.update_layout(
        template=colors.PLOTLY_TEMPLATE, paper_bgcolor=colors.BG, plot_bgcolor=colors.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="v", title="CHURN_REASON_CLEAN"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

# ------------------------------------------------------------------
# Row 3: Churn by tenure band (bar+line combo) | Churn by internet type (bar)
# ------------------------------------------------------------------
c3, c4 = st.columns(2)
with c3:
    chart_card_open("Churn_Rate_By_Tenure_Band")
    trates = churn_rate_by(fdf, "tenure_band", order=TENURE_ORDER)
    tenure_colors = [colors.MAROON if i % 2 == 0 else colors.GREY_FILL for i in range(len(trates))]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=trates.index, y=trates.values, marker_color=tenure_colors, showlegend=False))
    fig.add_trace(
        go.Scatter(
            x=trates.index, y=trates.values, mode="lines+markers+text",
            line=dict(color=colors.WHITE, width=2), marker=dict(color=colors.WHITE, size=6),
            text=trates.values, textposition="top center", textfont=dict(color=colors.WHITE),
            showlegend=False,
        )
    )
    fig.update_layout(
        template=colors.PLOTLY_TEMPLATE, paper_bgcolor=colors.BG, plot_bgcolor=colors.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Tenure_Band", yaxis_title="Churn_Rate", bargap=0,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

with c4:
    chart_card_open("Churn_Rate_By_Internet_Type")
    irates = churn_rate_by(fdf, "Internet Type", order=["Fiber Optic", "Cable", "DSL", "No Internet Service"])
    net_colors = [colors.ROSE if i % 2 == 0 else colors.PALE for i in range(len(irates))]
    fig = go.Figure(go.Bar(y=irates.index, x=irates.values, orientation="h", marker_color=net_colors, text=irates.values, textposition="outside"))
    fig.update_layout(
        template=colors.PLOTLY_TEMPLATE, paper_bgcolor=colors.BG, plot_bgcolor=colors.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Churn_Rate", yaxis_title="Internet_Type", yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

st.caption(
    "Computed live from the real Telco customer dataset (customer_account_status, "
    "customer_demographics, customer_location, customer_services, zipcode_population). "
    "All 3 slicers filter every chart and KPI on this page."
)
