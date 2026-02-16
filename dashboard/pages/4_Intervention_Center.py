"""
Page 4 — Intervention Center
Generate support messages, log actions, manage customer outreach.
"""
import streamlit as st
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils import (
    load_css, render_header, fetch_customer,
    generate_intervention_message, get_risk_reasons, risk_badge_large
)
from audit_log import append_audit_log, read_audit_log

st.set_page_config(page_title="Intervention Center — Equilibrate", page_icon="E", layout="wide")
load_css()

# ── Header ──
render_header()
st.markdown("# Intervention Center")

# ── Customer Selection ──
default_id = st.session_state.get("selected_customer_id", "")
in_col, _ = st.columns([1, 3])
with in_col:
    customer_id = st.text_input("Customer ID", value=default_id, placeholder="Enter ID", key="ic_id")

if not customer_id:
    st.info("Enter a Customer ID to generate a personalised intervention message. "
            "You can also navigate here from the Customer Profile page.")
    st.stop()

# ── Fetch ──
with st.spinner("Loading customer data..."):
    profile = fetch_customer(customer_id)

if not profile:
    st.warning(
        f"Customer record for ID {customer_id} is not yet available in the real-time stream. "
        "The account may not have recent transactions or the pipeline may still be processing."
    )
    st.stop()

risk_level = profile.get("risk_level", "UNKNOWN")
hardship_type = profile.get("hardship_type", "GENERAL")
risk_score = profile.get("risk_score", "N/A")
recommended_action = profile.get("recommended_action", "N/A")
hardship_display = str(hardship_type).replace("_", " ").title() if hardship_type not in ("N/A", "NONE", "GENERAL") else "General"

# ── Customer Summary ──
st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)
st.markdown("## Customer Summary")

s1, s2 = st.columns([3, 1])

with s1:
    st.markdown(f"""
    <div class="eq-card">
        <div class="eq-detail-row">
            <span class="eq-detail-label">Customer ID</span>
            <span class="eq-detail-value">{customer_id}</span>
        </div>
        <div class="eq-detail-row">
            <span class="eq-detail-label">Risk Score</span>
            <span class="eq-detail-value">{risk_score}</span>
        </div>
        <div class="eq-detail-row">
            <span class="eq-detail-label">Hardship Classification</span>
            <span class="eq-detail-value">{hardship_display}</span>
        </div>
        <div class="eq-detail-row" style="border-bottom:none;">
            <span class="eq-detail-label">Recommended Action</span>
            <span class="eq-detail-value">{recommended_action}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown(f"""
    <div class="eq-card" style="text-align:center; padding:28px 20px;">
        {risk_badge_large(risk_level)}
    </div>
    """, unsafe_allow_html=True)

# ── Risk Factors ──
with st.expander("View Risk Assessment Factors"):
    reasons = get_risk_reasons(profile)
    if reasons:
        for r_text in reasons:
            css_class = "eq-risk-factor-critical" if "abnormal" in r_text.lower() or "no recent" in r_text.lower() else "eq-risk-factor"
            st.markdown(f'<div class="{css_class}">{r_text}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="eq-risk-factor-ok">No significant risk factors identified.</div>',
                    unsafe_allow_html=True)

# ── Support Message ──
st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)
st.markdown("## Outreach Communication")
st.markdown(f"Auto-generated based on hardship classification: **{hardship_display}**")

message = generate_intervention_message(hardship_type, customer_id)
edited_message = st.text_area("Review and edit before sending:", value=message, height=250, key="ic_msg")

# ── Actions Row ──
st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)
st.markdown("## Actions")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("Send SMS", type="primary", use_container_width=True, key="ic_sms"):
        print(f"\n{'='*55}")
        print(f"  SMS SENT — Customer {customer_id}")
        print(f"  Risk Level: {risk_level} | Hardship: {hardship_type}")
        print(f"{'='*55}")
        print(edited_message)
        print(f"{'='*55}\n")

        append_audit_log(
            customer_id=customer_id,
            risk_level=risk_level,
            action_taken="SMS_SENT",
            message_sent=edited_message,
        )
        st.success(f"SMS successfully sent to Customer {customer_id}. Action logged to audit trail.")

with c2:
    if st.button("Mark as Reviewed", use_container_width=True, key="ic_review"):
        print(f"[REVIEWED] Customer {customer_id} marked as reviewed")
        append_audit_log(
            customer_id=customer_id,
            risk_level=risk_level,
            action_taken="MARKED_REVIEWED",
            message_sent="Officer reviewed customer profile",
        )
        st.success(f"Customer {customer_id} marked as reviewed.")

with c3:
    if st.button("Schedule Follow-up Call", use_container_width=True, key="ic_call"):
        print(f"[CALL] Follow-up call scheduled for Customer {customer_id}")
        append_audit_log(
            customer_id=customer_id,
            risk_level=risk_level,
            action_taken="CALL_SCHEDULED",
            message_sent="Follow-up call scheduled with customer",
        )
        st.success(f"Follow-up call scheduled for Customer {customer_id}.")

# ── Audit Trail ──
st.markdown('<div class="eq-section-divider"></div>', unsafe_allow_html=True)
st.markdown("## Audit Trail")

audit_df = read_audit_log()
if not audit_df.empty:
    st.dataframe(
        audit_df.sort_values("timestamp", ascending=False).head(25),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No audit entries recorded yet. Actions will be logged here after sending communications or reviews.")
