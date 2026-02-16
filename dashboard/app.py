"""
Equilibrate — Main Dashboard Entry Point v3.0
Professional banking operations console.
"""
import streamlit as st
import os, sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_css, render_header

# ─── Page Config ───
st.set_page_config(
    page_title="Equilibrate — Operations Console",
    page_icon="E",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Load Theme FIRST ───
load_css()

# ─── Sidebar ───
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-text">Equilibrate</div>
        <div class="sidebar-logo-sub">Operations Console</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # System Status
    st.markdown("##### System")
    import redis
    try:
        rc = redis.Redis(host="localhost", port=6379, decode_responses=True)
        rc.ping()
        customer_count = len(rc.keys("customer:*"))
        st.markdown(f"""
        <div class="sidebar-status"><span class="status-dot-green"></span> Redis Connected</div>
        <div class="sidebar-status" style="margin-left: 16px; color: #7BA3C9;">{customer_count:,} customers monitored</div>
        """, unsafe_allow_html=True)
    except Exception:
        st.markdown("""
        <div class="sidebar-status"><span class="status-dot-red"></span> Redis Disconnected</div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    now = datetime.now().strftime("%d %b %Y, %H:%M")
    st.caption(f"Last refreshed: {now}")
    st.caption("v3.0 — Real-Time Operations")

# ─── Main Content ───
render_header()

st.markdown("# Operations Hub")

# Feature cards with icons
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="eq-feature-card">
        <div class="eq-feature-icon" style="background: linear-gradient(135deg, #2E86DE, #1F4E79);">P</div>
        <div class="eq-feature-title">Portfolio Overview</div>
        <p class="eq-feature-desc">Real-time risk distribution, KPIs, and hardship trend analysis.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="eq-feature-card">
        <div class="eq-feature-icon" style="background: linear-gradient(135deg, #E74C3C, #C0392B);">R</div>
        <div class="eq-feature-title">Risk Queue</div>
        <p class="eq-feature-desc">Prioritised table of flagged customers requiring officer review.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="eq-feature-card">
        <div class="eq-feature-icon" style="background: linear-gradient(135deg, #F39C12, #E67E22);">C</div>
        <div class="eq-feature-title">Customer Profile</div>
        <p class="eq-feature-desc">360-degree customer view with risk explainability and financial behaviour.</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="eq-feature-card">
        <div class="eq-feature-icon" style="background: linear-gradient(135deg, #2ECC71, #27AE60);">I</div>
        <div class="eq-feature-title">Intervention Center</div>
        <p class="eq-feature-desc">Generate personalised support messages and log all outreach actions.</p>
    </div>
    """, unsafe_allow_html=True)

# Quick stats
st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)

try:
    rc = redis.Redis(host="localhost", port=6379, decode_responses=True)
    all_keys = rc.keys("customer:*")
    total = len(all_keys)

    # Quick count of risk levels
    high = 0
    medium = 0
    low = 0
    sample_keys = all_keys[:500]  # Sample for speed
    for k in sample_keys:
        rl = rc.hget(k, "risk_level")
        if rl == "HIGH":
            high += 1
        elif rl == "MEDIUM":
            medium += 1
        elif rl == "LOW":
            low += 1

    # Scale to full count
    if sample_keys:
        scale = total / len(sample_keys)
        high = int(high * scale)
        medium = int(medium * scale)
        low = int(low * scale)

    st.markdown("## Quick Summary")
    qc1, qc2, qc3, qc4 = st.columns(4)
    with qc1:
        st.metric("Total Customers", f"{total:,}")
    with qc2:
        st.metric("High Risk", f"{high:,}")
    with qc3:
        st.metric("Medium Risk", f"{medium:,}")
    with qc4:
        st.metric("Low Risk", f"{low:,}")
except Exception:
    st.info("Connect to Redis to view quick summary statistics.")

st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)
st.info("Select a section from the sidebar to begin operations.")
