"""Shared look-and-feel helpers so both pages match the Power BI export exactly."""

import streamlit as st
from data import BG, CARD_BORDER, BLACK, ROSE, GREY_TEXT, WHITE


def inject_css():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {BG};
        }}
        section[data-testid="stSidebar"] {{
            background-color: {BG};
            border-right: 1px solid {CARD_BORDER};
        }}
        .block-container {{
            padding-top: 1.5rem;
        }}
        .dash-title {{
            background-color: {BLACK};
            border-radius: 6px;
            padding: 16px 0;
            text-align: center;
            font-size: 30px;
            font-weight: 600;
            color: {WHITE};
            margin-bottom: 18px;
        }}
        .kpi-card {{
            background-color: {BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 6px;
            padding: 14px 20px;
            margin-bottom: 14px;
        }}
        .kpi-label {{
            color: {ROSE};
            font-size: 14px;
        }}
        .kpi-label-white {{
            color: {WHITE};
            font-size: 14px;
        }}
        .kpi-value {{
            color: {WHITE};
            font-size: 26px;
            font-weight: 700;
        }}
        .kpi-value-rose {{
            color: {ROSE};
            font-size: 26px;
            font-weight: 700;
        }}
        .chart-card {{
            background-color: {BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 6px;
            padding: 14px 16px 4px 16px;
            margin-bottom: 16px;
        }}
        .chart-title {{
            color: {WHITE};
            font-weight: 600;
            font-size: 15px;
            margin-bottom: 4px;
        }}
        .slicer-card {{
            background-color: {BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 6px;
            padding: 10px 14px;
            margin-bottom: 14px;
        }}
        .slicer-title {{
            color: {WHITE};
            font-weight: 600;
            font-size: 14px;
            margin-bottom: 6px;
        }}
        div[data-testid="stMetric"] {{
            background-color: {BG};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_title(text: str):
    st.markdown(f'<div class="dash-title">{text}</div>', unsafe_allow_html=True)


def kpi_card(label: str, value: str, rose_label: bool = False, rose_value: bool = False):
    label_cls = "kpi-label" if rose_label else "kpi-label-white"
    value_cls = "kpi-value-rose" if rose_value else "kpi-value"
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="{label_cls}">{label}</div>
            <div class="{value_cls}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_card_open(title: str):
    st.markdown(f'<div class="chart-card"><div class="chart-title">{title}</div>', unsafe_allow_html=True)


def chart_card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def slicer_open(title: str):
    st.markdown(f'<div class="slicer-card"><div class="slicer-title">{title}</div>', unsafe_allow_html=True)


def slicer_close():
    st.markdown("</div>", unsafe_allow_html=True)
