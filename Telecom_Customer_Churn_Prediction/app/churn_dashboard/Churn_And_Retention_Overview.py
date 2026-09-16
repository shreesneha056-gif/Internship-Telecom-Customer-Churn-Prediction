import streamlit as st
import plotly.graph_objects as go

import data as d
from style import inject_css, page_title, kpi_card, chart_card_open, chart_card_close, slicer_open, slicer_close

st.set_page_config(page_title="Churn And Retention Overview", layout="wide", page_icon="📉")
inject_css()

# ------------------------------------------------------------------
# Sidebar — slicers (mirrors the Power BI slicer panel)
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🔴 Clear_All_Slicers")
    if st.button("Clear_All_Slicers", use_container_width=True):
        st.session_state["contract_filter"] = d.CONTRACT_OPTIONS
        st.session_state["internet_filter"] = d.INTERNET_SERVICE_OPTIONS
        st.session_state["payment_filter"] = d.PAYMENT_METHOD_OPTIONS

    slicer_open("Contract_Type")
    contract_filter = st.multiselect(
        "Contract_Type", d.CONTRACT_OPTIONS, default=d.CONTRACT_OPTIONS,
        label_visibility="collapsed", key="contract_filter",
    )
    slicer_close()

    slicer_open("Internet_Service")
    internet_filter = st.multiselect(
        "Internet_Service", d.INTERNET_SERVICE_OPTIONS, default=d.INTERNET_SERVICE_OPTIONS,
        label_visibility="collapsed", key="internet_filter",
    )
    slicer_close()

    slicer_open("Payment_Method")
    payment_filter = st.multiselect(
        "Payment_Method", d.PAYMENT_METHOD_OPTIONS, default=d.PAYMENT_METHOD_OPTIONS,
        label_visibility="collapsed", key="payment_filter",
    )
    slicer_close()

page_title("Churn_And_Retention_Overview")

# ------------------------------------------------------------------
# KPI row
# ------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total_Customers", d.KPI_CHURN["Total_Customers"], rose_label=True, rose_value=False)
with k2:
    kpi_card("Churn_Rate_In_Per", d.KPI_CHURN["Churn_Rate_In_Per"], rose_label=False, rose_value=True)
with k3:
    kpi_card("Avg_Tenure_In_Per", d.KPI_CHURN["Avg_Tenure_In_Per"], rose_label=True, rose_value=False)
with k4:
    kpi_card("Churned_Customers", d.KPI_CHURN["Churned_Customers"], rose_label=False, rose_value=True)

# ------------------------------------------------------------------
# Row 2: Churn by contract (bar) | Top 5 churn reasons (donut)
# ------------------------------------------------------------------
contract_df = d.churn_by_contract[d.churn_by_contract["Contract"].isin(contract_filter)] \
    if contract_filter else d.churn_by_contract

c1, c2 = st.columns(2)
with c1:
    chart_card_open("Churn_Rate_By_Contract")
    fig = go.Figure(
        go.Bar(
            x=contract_df["Contract"], y=contract_df["Churn_Rate"],
            marker_color=contract_df["color"],
            text=contract_df["Churn_Rate"], textposition="outside",
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Contract", yaxis_title="Churn_Rate",
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

with c2:
    chart_card_open("Top_5_Churn_Reason_For_Churn")
    fig = go.Figure(
        go.Pie(
            labels=d.churn_reason["CHURN_REASON_CLEAN"], values=d.churn_reason["pct"], hole=0.55,
            marker=dict(colors=d.DONUT_COLORS),
            textinfo="percent", sort=False,
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="v", title="CHURN_REASON_CLEAN"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

# ------------------------------------------------------------------
# Row 3: Churn by tenure band (area) | Churn by internet type (bar)
# ------------------------------------------------------------------
c3, c4 = st.columns(2)
with c3:
    chart_card_open("Churn_Rate_By_Tenure_Band")
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=d.churn_by_tenure["Tenure_Band"], y=d.churn_by_tenure["Churn_Rate"],
            marker_color=d.churn_by_tenure["color"], showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=d.churn_by_tenure["Tenure_Band"], y=d.churn_by_tenure["Churn_Rate"],
            mode="lines+markers+text",
            line=dict(color=d.WHITE, width=2),
            marker=dict(color=d.WHITE, size=6),
            text=d.churn_by_tenure["Churn_Rate"], textposition="top center",
            textfont=dict(color=d.WHITE),
            showlegend=False,
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Tenure_Band", yaxis_title="Churn_Rate",
        bargap=0,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

with c4:
    internet_df = d.churn_by_internet
    chart_card_open("Churn_Rate_By_Internet_Type")
    fig = go.Figure(
        go.Bar(
            y=internet_df["Internet_Type"], x=internet_df["Churn_Rate"], orientation="h",
            marker_color=internet_df["color"],
            text=internet_df["Churn_Rate"], textposition="outside",
        )
    )
    fig.update_layout(
        template=d.PLOTLY_TEMPLATE, paper_bgcolor=d.BG, plot_bgcolor=d.BG,
        height=340, margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Churn_Rate", yaxis_title="Internet_Type",
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    chart_card_close()

st.caption(
    "Rebuilt from the exported Power BI report (PowerBI.pbix / dashboard.pdf). "
    "Contract_Type, Internet_Service and Payment_Method filters are shown for layout "
    "parity; Contract_Type is live against the Churn_Rate_By_Contract chart."
)
