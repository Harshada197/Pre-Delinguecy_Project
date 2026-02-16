"""
Page 3 — Customer 360 Profile
Professional banking layout with split sections.
"""
import streamlit as st
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import load_css, render_header, fetch_customer, get_risk_reasons, risk_badge_large

st.set_page_config(page_title="Customer Profile — Equilibrate", page_icon="E", layout="wide")
load_css()

# ── Auto Refresh ──
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, limit=None, key="profile_refresh")

# ── Header ──
render_header()
st.markdown("# Customer 360 Profile")

# ── Input ──
default_id = st.session_state.get("selected_customer_id", "")
in_col, _ = st.columns([1, 3])
with in_col:
    customer_id = st.text_input("Customer ID", value=default_id, placeholder="Enter ID", key="cp_id")

if not customer_id:
    st.info("Enter a Customer ID above to load their profile. You can also select a customer from the Risk Queue.")
    st.stop()

# ── Fetch ──
with st.spinner("Loading customer profile..."):
    profile = fetch_customer(customer_id)

if not profile:
    st.warning(
        f"Customer record for ID {customer_id} is not yet available in the real-time stream. "
        "The account may not have recent transactions or the data pipeline may still be processing."
    )
    st.stop()

# ── Parse ──
risk_level = profile.get("risk_level", "UNKNOWN")
risk_score = profile.get("risk_score", "N/A")
txn_count = int(profile.get("txn_count", 0))
salary_count = int(profile.get("salary_count", 0))
withdrawals = int(profile.get("withdrawals", 0))
total_spend = float(profile.get("total_spend", 0))
essential_spend = float(profile.get("essential_spend", 0))
discretionary_spend = float(profile.get("discretionary_spend", 0))
hardship_type = profile.get("hardship_type", "N/A")
recommended_action = profile.get("recommended_action", "N/A")
last_salary = profile.get("last_salary_ts", "")
city = profile.get("city", "N/A")
employment = profile.get("employment_type", "N/A")
age = profile.get("age", "N/A")
salary = profile.get("salary", "N/A")
emi = profile.get("emi_amount", "N/A")
hardship_display = str(hardship_type).replace("_", " ").title() if hardship_type not in ("N/A", "NONE") else "None"

# ═══════════════════════════════════════
# ROW 1: Customer Details (left) + Risk Badge (right)
# ═══════════════════════════════════════
st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)

left_col, right_col = st.columns([3, 1])

with left_col:
    st.markdown("## Customer Details")
    st.markdown(f"""
    <div class="eq-card">
        <div class="eq-detail-row">
            <span class="eq-detail-label">Customer ID</span>
            <span class="eq-detail-value">{customer_id}</span>
        </div>
        <div class="eq-detail-row">
            <span class="eq-detail-label">City</span>
            <span class="eq-detail-value">{city}</span>
        </div>
        <div class="eq-detail-row">
            <span class="eq-detail-label">Age</span>
            <span class="eq-detail-value">{age}</span>
        </div>
        <div class="eq-detail-row">
            <span class="eq-detail-label">Employment Type</span>
            <span class="eq-detail-value">{employment}</span>
        </div>
        <div class="eq-detail-row">
            <span class="eq-detail-label">Monthly Salary</span>
            <span class="eq-detail-value">Rs. {salary}</span>
        </div>
        <div class="eq-detail-row" style="border-bottom:none;">
            <span class="eq-detail-label">EMI Amount</span>
            <span class="eq-detail-value">Rs. {emi}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with right_col:
    st.markdown("## Risk Assessment")
    st.markdown(f"""
    <div class="eq-card" style="text-align:center; padding:32px 20px;">
        <div style="margin-bottom:20px;">
            {risk_badge_large(risk_level)}
        </div>
        <div class="eq-stat-value" style="font-size:2.8rem; margin-bottom:2px;">{risk_score}</div>
        <div class="eq-stat-label">Risk Score</div>
        <div style="margin-top:24px; border-top:1px solid #F0F2F5; padding-top:18px;">
            <div class="eq-stat-label">Hardship Type</div>
            <div style="font-size:0.95rem; font-weight:700; color:#1F4E79; margin-top:6px;">{hardship_display}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════
# ROW 2: Financial Behaviour
# ═══════════════════════════════════════
st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)
st.markdown("## Financial Behaviour")

fc1, fc2, fc3, fc4 = st.columns(4)
with fc1:
    st.markdown(f"""
    <div class="eq-card" style="text-align:center;">
        <div class="eq-stat-value">{txn_count}</div>
        <div class="eq-stat-label">Transactions</div>
    </div>
    """, unsafe_allow_html=True)
with fc2:
    st.markdown(f"""
    <div class="eq-card" style="text-align:center;">
        <div class="eq-stat-value">{salary_count}</div>
        <div class="eq-stat-label">Salary Credits</div>
    </div>
    """, unsafe_allow_html=True)
with fc3:
    st.markdown(f"""
    <div class="eq-card" style="text-align:center;">
        <div class="eq-stat-value">{withdrawals}</div>
        <div class="eq-stat-label">ATM Withdrawals</div>
    </div>
    """, unsafe_allow_html=True)
with fc4:
    st.markdown(f"""
    <div class="eq-card" style="text-align:center;">
        <div class="eq-stat-value">Rs. {total_spend:,.0f}</div>
        <div class="eq-stat-label">Total Spend</div>
    </div>
    """, unsafe_allow_html=True)

# ── Spending Breakdown ──
sp1, sp2 = st.columns(2)
with sp1:
    st.markdown(f"""
    <div class="eq-card">
        <div class="eq-card-header">Essential Spending</div>
        <div class="eq-stat-value" style="color:#E74C3C;">Rs. {essential_spend:,.0f}</div>
        <div class="eq-stat-label" style="margin-top:8px;">Groceries, utilities, rent, medical</div>
    </div>
    """, unsafe_allow_html=True)
with sp2:
    st.markdown(f"""
    <div class="eq-card">
        <div class="eq-card-header">Discretionary Spending</div>
        <div class="eq-stat-value" style="color:#2ECC71;">Rs. {discretionary_spend:,.0f}</div>
        <div class="eq-stat-label" style="margin-top:8px;">Shopping, travel, dining, entertainment</div>
    </div>
    """, unsafe_allow_html=True)

if last_salary and last_salary.strip():
    st.markdown(f"""
    <div class="eq-card">
        <div class="eq-detail-row" style="border-bottom:none;">
            <span class="eq-detail-label">Last Salary Credit</span>
            <span class="eq-detail-value">{last_salary}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════
# ROW 3: Risk Explainability
# ═══════════════════════════════════════
st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)
st.markdown("## Risk Assessment Factors")

reasons = get_risk_reasons(profile)
if reasons:
    for reason in reasons:
        css_class = "eq-risk-factor-critical" if "abnormal" in reason.lower() or "no recent" in reason.lower() else "eq-risk-factor"
        st.markdown(f'<div class="{css_class}">{reason}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="eq-risk-factor-ok">No significant risk factors detected for this customer.</div>',
                unsafe_allow_html=True)

# ═══════════════════════════════════════
# ROW 4: Recommended Action
# ═══════════════════════════════════════
if recommended_action and recommended_action not in ("N/A", "Continue monitoring"):
    st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## Recommended Action")
    st.info(recommended_action)

# ── Navigation ──
st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)
if st.button("Proceed to Intervention Center", type="primary"):
    st.session_state["selected_customer_id"] = customer_id
    st.success("Navigate to Intervention Center from the sidebar to send a support communication.")
