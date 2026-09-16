import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils import (
    load_data, kpi_card, panel_start, panel_end, base_layout, alt_colors,
    DONUT_PALETTE, ACCENT, SECONDARY, TEXT_MAIN, TEXT_MUTED, BG_COLOR,
    PANEL_BG, PANEL_BORDER, format_k,
)

st.set_page_config(
    page_title="Churn And Retention Overview",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Global CSS - dark theme matching the source Power BI report
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
        .stApp {{ background-color: {BG_COLOR}; }}
        section[data-testid="stSidebar"] {{ background-color: {PANEL_BG};
            border-right: 1px solid {PANEL_BORDER}; }}
        div[data-testid="stVerticalBlock"] > div:has(> div.title-bar) {{ margin-bottom: 0; }}
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
# Sidebar - slicers (Contract_Type, Internet_Service, Payment_Method)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧹 Clear_All_Slicers")
    if st.button("Clear All Slicers", use_container_width=True):
        for k in ["contract_f", "internet_f", "payment_f"]:
            st.session_state.pop(k, None)
        st.rerun()

    st.markdown("#### Contract_Type")
    contract_opts = sorted(df["Contract"].dropna().unique().tolist())
    contract_f = st.multiselect("Contract_Type", contract_opts, default=[], key="contract_f",
                                 label_visibility="collapsed")

    st.markdown("#### Internet_Service")
    internet_f = st.radio("Internet_Service", ["All", "True", "False"], index=0,
                           key="internet_f", label_visibility="collapsed")

    st.markdown("#### Payment_Method")
    payment_opts = sorted(df["Payment Method"].dropna().unique().tolist())
    payment_f = st.multiselect("Payment_Method", payment_opts, default=[], key="payment_f",
                                label_visibility="collapsed")

# ---------------------------------------------------------------------------
# Apply filters
# ---------------------------------------------------------------------------
fdf = df.copy()
if contract_f:
    fdf = fdf[fdf["Contract"].isin(contract_f)]
if internet_f != "All":
    want = internet_f == "True"
    fdf = fdf[(fdf["Internet Service"] == "Yes") == want]
if payment_f:
    fdf = fdf[fdf["Payment Method"].isin(payment_f)]

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
st.markdown('<div class="title-bar">Churn_And_Retention_Overview</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
total_customers = fdf["Customer ID"].nunique()
churned_customers = int(fdf["Is_Churned"].sum())
churn_rate_val = round(churned_customers / total_customers * 100, 2) if total_customers else 0
avg_tenure_val = round(fdf["Tenure in Months"].mean(), 2) if total_customers else 0

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total_Customers", format_k(total_customers), SECONDARY)
with k2:
    kpi_card("Churn_Rate_In_Per", f"{churn_rate_val}", ACCENT)
with k3:
    kpi_card("Avg_Tenure_In_Per", f"{avg_tenure_val}", ACCENT)
with k4:
    kpi_card("Churned_Customers", format_k(churned_customers), ACCENT)

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Row 1: Churn_Rate_By_Contract | Top_5_Churn_Reason_For_Churn
# ---------------------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    panel_start("Churn_Rate_By_Contract")
    g = (
        fdf.groupby("Contract")["Is_Churned"]
        .mean().mul(100).round(0).reset_index(name="Churn_Rate")
        .sort_values("Churn_Rate", ascending=False)
    )
    fig = go.Figure(
        go.Bar(
            x=g["Contract"], y=g["Churn_Rate"],
            text=g["Churn_Rate"].astype(int), textposition="outside",
            marker_color=alt_colors(len(g)),
        )
    )
    fig.update_layout(yaxis_title="Churn_Rate", xaxis_title="Contract")
    st.plotly_chart(base_layout(fig), use_container_width=True, config={"displayModeBar": False})
    panel_end()

with c2:
    panel_start("Top_5_Churn_Reason_For_Churn")
    churned_only = fdf[fdf["Is_Churned"] & fdf["Churn Reason"].notna()]
    g = (
        churned_only["Churn Reason"].value_counts()
        .head(5).reset_index()
    )
    g.columns = ["Churn Reason", "count"]
    fig = go.Figure(
        go.Pie(
            labels=g["Churn Reason"], values=g["count"], hole=0.55,
            marker=dict(colors=DONUT_PALETTE[: len(g)]),
            textinfo="percent", textfont_color="#FFFFFF",
        )
    )
    fig.update_layout(showlegend=True, legend=dict(font=dict(color=TEXT_MAIN, size=10)))
    st.plotly_chart(base_layout(fig, height=340), use_container_width=True, config={"displayModeBar": False})
    panel_end()

# ---------------------------------------------------------------------------
# Row 2: Churn_Rate_By_Tenure_Band | Churn_Rate_By_Internet_Type
# ---------------------------------------------------------------------------
c3, c4 = st.columns(2)

with c3:
    panel_start("Churn_Rate_By_Tenure_Band")
    order = ["0-12 months", "12-24 months", "24-48 months", "48+ months"]
    g = (
        fdf.groupby("Tenure_Band")["Is_Churned"]
        .mean().mul(100).round(0).reindex(order).reset_index(name="Churn_Rate")
    )
    colors = alt_colors(len(g))
    fig = go.Figure()
    for i in range(len(g)):
        seg = g.iloc[max(0, i - 1): i + 1]
        fig.add_trace(go.Scatter(
            x=seg["Tenure_Band"], y=seg["Churn_Rate"], fill="tozeroy",
            mode="lines", line=dict(color="#FFFFFF", width=2),
            fillcolor=colors[i], showlegend=False,
        ))
    for i, row in g.iterrows():
        fig.add_annotation(x=row["Tenure_Band"], y=row["Churn_Rate"] + 3,
                            text=str(int(row["Churn_Rate"])), showarrow=False,
                            font=dict(color=TEXT_MAIN, size=12))
    fig.update_layout(yaxis_title="Churn_Rate", xaxis_title="Tenure_Band")
    st.plotly_chart(base_layout(fig), use_container_width=True, config={"displayModeBar": False})
    panel_end()

with c4:
    panel_start("Churn_Rate_By_Internet_Type")
    g = (
        fdf.groupby("Internet Type")["Is_Churned"]
        .mean().mul(100).round(0).reset_index(name="Churn_Rate")
        .sort_values("Churn_Rate", ascending=False)
    )
    fig = go.Figure(
        go.Bar(
            x=g["Churn_Rate"], y=g["Internet Type"], orientation="h",
            text=g["Churn_Rate"].astype(int), textposition="outside",
            marker_color=alt_colors(len(g)),
        )
    )
    fig.update_layout(yaxis_title="Internet_Type", xaxis_title="Churn_Rate",
                       yaxis=dict(autorange="reversed"))
    st.plotly_chart(base_layout(fig), use_container_width=True, config={"displayModeBar": False})
    panel_end()
