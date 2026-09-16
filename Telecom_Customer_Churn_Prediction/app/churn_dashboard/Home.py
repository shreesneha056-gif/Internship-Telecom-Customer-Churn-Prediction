import streamlit as st
import plotly.graph_objects as go
from utils import (
    load_data, inject_css, kpi_card, chart_title, page_title, churn_rate_by,
    PLOTLY_LAYOUT, ROSE, ROSE_DARK, WHITE_BAR, GRAY_BAR, DONUT_COLORS,
)

st.set_page_config(page_title="Churn And Retention Overview", layout="wide", page_icon="📊")
inject_css()

df = load_data()

# ----------------------------- SIDEBAR SLICERS -----------------------------
with st.sidebar:
    if st.button("🔴  Clear All Slicers", use_container_width=True):
        for k in ["contract_f", "internet_f", "payment_f"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

    st.markdown("**Contract_Type**")
    contract_opts = ["Month-to-Month", "One Year", "Two Year"]
    contract_f = st.multiselect("Contract_Type", contract_opts, default=contract_opts,
                                 key="contract_f", label_visibility="collapsed")

    st.markdown("**Internet_Service**")
    internet_f = st.radio("Internet_Service", ["All", "True", "False"], horizontal=True,
                           key="internet_f", label_visibility="collapsed")

    st.markdown("**Payment_Method**")
    payment_opts = ["Bank Withdrawal", "Credit Card", "Mailed Check"]
    payment_f = st.multiselect("Payment_Method", payment_opts, default=payment_opts,
                                key="payment_f", label_visibility="collapsed")

# ----------------------------- FILTER DATA -----------------------------
fdf = df[df["Contract"].isin(contract_f) & df["Payment Method"].isin(payment_f)]
if internet_f == "True":
    fdf = fdf[fdf["Internet Service"] == "Yes"]
elif internet_f == "False":
    fdf = fdf[fdf["Internet Service"] == "No"]

# ----------------------------- TITLE -----------------------------
page_title("Churn_And_Retention_Overview")

# ----------------------------- KPI ROW -----------------------------
total_customers = len(fdf)
churn_rate = round(100 * fdf["Is_Churned"].sum() / total_customers, 2) if total_customers else 0
avg_tenure = round(fdf["Tenure in Months"].mean(), 2) if total_customers else 0
churned_customers = int(fdf["Is_Churned"].sum())

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Total_Customers", f"{total_customers/1000:.0f}K" if total_customers >= 1000 else total_customers)
with c2:
    kpi_card("Churn_Rate_In_Per", f"{churn_rate}")
with c3:
    kpi_card("Avg_Tenure_In_Per", f"{avg_tenure}")
with c4:
    kpi_card("Churned_Customers", f"{churned_customers/1000:.0f}K" if churned_customers >= 1000 else churned_customers)

st.write("")

# ----------------------------- ROW 1: Contract | Churn Reasons -----------------------------
row1_left, row1_right = st.columns(2)

with row1_left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_title("Churn_Rate_By_Contract")
    g = churn_rate_by(fdf, "Contract", order=["Month-to-Month", "One Year", "Two Year"])
    fig = go.Figure(go.Bar(
        x=g["Contract"], y=g["Churn_Rate"], marker_color=ROSE,
        text=g["Churn_Rate"].astype(int), textposition="outside",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=320,
                       yaxis_title="Churn_Rate", xaxis_title="Contract")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with row1_right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_title("Top_5_Churn_Reason_For_Churn")
    reason_counts = fdf["Churn_Reason_Clean"].value_counts()
    if len(reason_counts):
        fig = go.Figure(go.Pie(
            labels=reason_counts.index, values=reason_counts.values, hole=0.55,
            marker=dict(colors=DONUT_COLORS[:len(reason_counts)]),
            textinfo="percent", textfont=dict(color="white"),
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=320,
                           legend=dict(title="CHURN_REASON_CLEAN", font=dict(size=10)))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No churned customers in current filter selection.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------- ROW 2: Tenure Band | Internet Type -----------------------------
row2_left, row2_right = st.columns(2)

with row2_left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_title("Churn_Rate_By_Tenure_Band")
    order = ["0-12 months", "12-24 months", "24-48 months", "48+ months"]
    g = churn_rate_by(fdf, "Tenure_Band", order=order)
    bar_colors = [ROSE_DARK, GRAY_BAR, ROSE_DARK, GRAY_BAR]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=g["Tenure_Band"], y=g["Churn_Rate"], marker_color=bar_colors,
                          text=g["Churn_Rate"].astype(int), textposition="outside", showlegend=False))
    fig.add_trace(go.Scatter(x=g["Tenure_Band"], y=g["Churn_Rate"], mode="lines",
                              line=dict(color="white", width=2), showlegend=False))
    fig.update_layout(**PLOTLY_LAYOUT, height=320,
                       yaxis_title="Churn_Rate", xaxis_title="Tenure_Band")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with row2_right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_title("Churn_Rate_By_Internet_Type")
    order = ["Fiber Optic", "Cable", "DSL", "No Internet Service"]
    g = churn_rate_by(fdf, "Internet_Type_Clean", order=order)
    bar_colors = [ROSE, WHITE_BAR, ROSE, WHITE_BAR]
    fig = go.Figure(go.Bar(
        x=g["Churn_Rate"], y=g["Internet_Type_Clean"], orientation="h",
        marker_color=bar_colors, text=g["Churn_Rate"].astype(int), textposition="outside",
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=320,
                       xaxis_title="Churn_Rate", yaxis_title="Internet_Type",
                       yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
