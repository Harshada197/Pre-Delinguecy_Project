"""
Page 2 — Risk Queue
Prioritised table of at-risk customers for officer review.
"""
import streamlit as st
import pandas as pd
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import load_css, render_header, render_live_tag, fetch_all_customers

st.set_page_config(page_title="Risk Queue — Equilibrate", page_icon="E", layout="wide")
load_css()

# ── Auto Refresh ──
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, limit=None, key="queue_refresh")

# ── Header ──
render_header()

title_col, live_col = st.columns([4, 1])
with title_col:
    st.markdown("# Risk Queue")
with live_col:
    st.markdown("<br>", unsafe_allow_html=True)
    render_live_tag()

# ── Data ──
with st.spinner("Loading customer risk data from Redis..."):
    df = fetch_all_customers()

if df.empty:
    st.warning("No customer data is currently available in the real-time stream. "
               "Ensure the data pipeline and risk engine are running.")
    st.stop()

# ── Filters ──
st.markdown("## Filters")
f_col1, f_col2, f_col3 = st.columns([1, 1, 2])

with f_col1:
    risk_filter = st.selectbox(
        "Risk Level",
        options=["High & Medium", "High Only", "Medium Only", "All Customers"],
        index=0, key="rq_risk_filter",
    )

with f_col2:
    search_id = st.text_input("Customer ID", placeholder="Search...", key="rq_search")

# ── Apply filters ──
filtered = df.copy()
if "risk_level" in filtered.columns:
    if risk_filter == "High Only":
        filtered = filtered[filtered["risk_level"] == "HIGH"]
    elif risk_filter == "Medium Only":
        filtered = filtered[filtered["risk_level"] == "MEDIUM"]
    elif risk_filter == "High & Medium":
        filtered = filtered[filtered["risk_level"].isin(["HIGH", "MEDIUM"])]

if search_id:
    filtered = filtered[filtered["customer_id"].astype(str).str.contains(str(search_id))]

# Sort by risk score descending
if "risk_score" in filtered.columns:
    filtered = filtered.sort_values("risk_score", ascending=False)

# ── Summary Metrics ──
st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)
st.markdown("## Queue Summary")
mc1, mc2, mc3 = st.columns(3)
with mc1:
    st.metric("Customers in Queue", f"{len(filtered):,}")
with mc2:
    h_count = len(filtered[filtered["risk_level"] == "HIGH"]) if "risk_level" in filtered.columns else 0
    st.metric("High Risk", f"{h_count:,}")
with mc3:
    m_count = len(filtered[filtered["risk_level"] == "MEDIUM"]) if "risk_level" in filtered.columns else 0
    st.metric("Medium Risk", f"{m_count:,}")

# ── Table ──
st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)
st.markdown("## Customer Risk Table")

if filtered.empty:
    st.info("No customers match the selected filter criteria.")
else:
    # Build display columns
    display_cols = []
    col_names = {}

    available = {
        "customer_id": "Customer ID",
        "risk_level": "Risk Level",
        "risk_score": "Risk Score",
        "hardship_type": "Hardship Type",
        "recommended_action": "Recommended Action",
        "city": "City",
        "employment_type": "Employment",
        "salary_count": "Salary Credits",
        "withdrawals": "Withdrawals",
    }

    for col, label in available.items():
        if col in filtered.columns:
            display_cols.append(col)
            col_names[col] = label

    display_df = filtered[display_cols].rename(columns=col_names).reset_index(drop=True)

    # Clean up hardship type display
    if "Hardship Type" in display_df.columns:
        display_df["Hardship Type"] = display_df["Hardship Type"].apply(
            lambda x: str(x).replace("_", " ").title() if pd.notna(x) and x != "NONE" else "None"
        )

    # Style risk level cells
    def style_risk(val):
        colors = {
            "HIGH": "background-color: #E74C3C; color: white; font-weight: 600; text-align: center; border-radius: 4px;",
            "MEDIUM": "background-color: #F39C12; color: white; font-weight: 600; text-align: center; border-radius: 4px;",
            "LOW": "background-color: #2ECC71; color: white; font-weight: 600; text-align: center; border-radius: 4px;",
        }
        return colors.get(str(val).upper().strip(), "")

    styled = display_df.style
    if "Risk Level" in display_df.columns:
        styled = styled.map(style_risk, subset=["Risk Level"])

    st.dataframe(styled, use_container_width=True, height=480, hide_index=True)

    st.caption(f"Showing {len(display_df):,} of {len(df):,} customers")

    # ── Profile Navigation ──
    st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## Quick Profile Access")
    nav_c1, nav_c2 = st.columns([2, 1])

    with nav_c1:
        selected_id = st.selectbox(
            "Select Customer",
            options=filtered["customer_id"].tolist(),
            index=0, key="rq_nav_select",
        )
    with nav_c2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("View Profile", type="primary", use_container_width=True):
            st.session_state["selected_customer_id"] = selected_id
            st.success(f"Customer {selected_id} selected. Open Customer Profile page from the sidebar.")
