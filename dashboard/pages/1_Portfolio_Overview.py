"""
Page 1 — Portfolio Overview
Real-time risk distribution and portfolio health monitoring.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import load_css, render_header, render_live_tag, fetch_all_customers, risk_counts, hardship_distribution

st.set_page_config(page_title="Portfolio Overview — Equilibrate", page_icon="E", layout="wide")
load_css()

# ── Auto Refresh ──
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, limit=None, key="portfolio_refresh")

# ── Header ──
render_header()

title_col, live_col = st.columns([4, 1])
with title_col:
    st.markdown("# Portfolio Overview")
with live_col:
    st.markdown("<br>", unsafe_allow_html=True)
    render_live_tag()

# ── Data ──
df = fetch_all_customers()

if df.empty:
    st.warning("No customer data is currently available in the real-time stream. "
               "Ensure the Kafka pipeline and feature engine are running.")
    st.stop()

counts = risk_counts(df)
total = len(df)

# ── KPI Metrics ──
st.markdown("## Key Risk Indicators")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Customers", f"{total:,}")
with col2:
    st.metric("High Risk", f"{counts['HIGH']:,}")
with col3:
    st.metric("Medium Risk", f"{counts['MEDIUM']:,}")
with col4:
    st.metric("Low Risk", f"{counts['LOW']:,}")

# ── Charts Row ──
st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)
chart_col1, chart_col2 = st.columns(2)

CHART_FONT = dict(family="Inter, Segoe UI, sans-serif", color="#2C3E50")
CHART_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=CHART_FONT,
    margin=dict(t=30, b=30, l=30, r=30),
)

with chart_col1:
    st.markdown("## Risk Distribution")

    fig_pie = go.Figure(data=[go.Pie(
        labels=["HIGH", "MEDIUM", "LOW"],
        values=[counts["HIGH"], counts["MEDIUM"], counts["LOW"]],
        marker=dict(
            colors=["#E74C3C", "#F39C12", "#2ECC71"],
            line=dict(color="#FFFFFF", width=2),
        ),
        hole=0.55,
        textinfo="value+percent",
        textfont=dict(size=13, family="Inter, sans-serif"),
        insidetextorientation="radial",
    )])

    fig_pie.update_layout(
        **CHART_LAYOUT,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5,
                    font=dict(size=12, family="Inter, sans-serif")),
        annotations=[
            dict(text=f"<b>{total:,}</b><br><span style='font-size:11px;color:#7F8C9B'>Total</span>",
                 x=0.5, y=0.5, font_size=20, font_family="Inter, sans-serif",
                 showarrow=False, font_color="#0B1F3A")
        ],
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    st.markdown("## Hardship Classification")
    hardship = hardship_distribution(df)

    if hardship:
        labels = [h.replace("_", " ").title() for h in hardship.keys()]
        values = list(hardship.values())

        fig_bar = go.Figure(data=[go.Bar(
            x=labels, y=values,
            marker=dict(
                color=["#1F4E79", "#2E86DE", "#E74C3C", "#F39C12", "#2ECC71"][:len(labels)],
                line=dict(width=0),
            ),
            text=values,
            textposition="outside",
            textfont=dict(size=12, family="Inter, sans-serif", color="#2C3E50"),
        )])

        fig_bar.update_layout(
            **CHART_LAYOUT,
            showlegend=False,
            xaxis=dict(showgrid=False, tickfont=dict(size=11, family="Inter, sans-serif")),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)",
                       tickfont=dict(size=11, family="Inter, sans-serif")),
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Hardship classification data will appear once the risk engine has evaluated customer profiles.")

# ── Risk Score Distribution ──
if "risk_score" in df.columns:
    st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## Risk Score Distribution")

    fig_hist = go.Figure(data=[go.Histogram(
        x=df["risk_score"],
        nbinsx=15,
        marker=dict(
            color="#2E86DE",
            line=dict(color="#1F4E79", width=1),
        ),
    )])

    fig_hist.update_layout(
        **CHART_LAYOUT,
        xaxis=dict(title="Risk Score", showgrid=False,
                   tickfont=dict(size=11, family="Inter, sans-serif"),
                   titlefont=dict(size=12, family="Inter, sans-serif", color="#5A6C7E")),
        yaxis=dict(title="Number of Customers", showgrid=True, gridcolor="rgba(0,0,0,0.06)",
                   tickfont=dict(size=11, family="Inter, sans-serif"),
                   titlefont=dict(size=12, family="Inter, sans-serif", color="#5A6C7E")),
        bargap=0.05,
    )
    st.plotly_chart(fig_hist, use_container_width=True)
