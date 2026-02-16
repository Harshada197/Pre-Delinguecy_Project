"""
Equilibrate — Dashboard Utilities v3.0
Redis data access, risk analysis, badge rendering, and CSS loader.
"""
import redis
import pandas as pd
import os
import streamlit as st


# ── Redis Connection ──
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# ── Paths ──
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles", "theme.css")
CUSTOMERS_CSV = os.path.join(PROJECT_ROOT, "data", "customers.csv")


# ═══════════════════════════════════════════════
# CSS & HEADER
# ═══════════════════════════════════════════════

def load_css():
    """Load the external CSS theme file."""
    if os.path.isfile(CSS_PATH):
        with open(CSS_PATH, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_header():
    """Render the professional platform header banner."""
    st.markdown("""
    <div class="eq-header">
        <div class="eq-header-title">EQUILIBRATE</div>
        <div class="eq-header-divider"></div>
        <div class="eq-header-subtitle">Pre-Delinquency Intervention Engine &bull; Internal Operations Console</div>
    </div>
    """, unsafe_allow_html=True)


def render_live_tag():
    """Show a live data indicator."""
    st.markdown("""
    <div class="live-indicator">
        <span class="live-dot"></span> Live Data
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# BADGE RENDERING
# ═══════════════════════════════════════════════

def risk_badge(level: str) -> str:
    """Return HTML for a styled risk badge."""
    level = str(level).upper().strip()
    badge_map = {
        "HIGH": '<span class="badge-high">HIGH RISK</span>',
        "MEDIUM": '<span class="badge-medium">MEDIUM RISK</span>',
        "LOW": '<span class="badge-low">LOW RISK</span>',
    }
    return badge_map.get(level, f'<span class="badge-unknown">{level}</span>')


def risk_badge_large(level: str) -> str:
    """Return HTML for a large styled risk badge (profile page)."""
    level = str(level).upper().strip()
    badge_map = {
        "HIGH": '<span class="badge-high-lg">HIGH RISK</span>',
        "MEDIUM": '<span class="badge-medium-lg">MEDIUM RISK</span>',
        "LOW": '<span class="badge-low-lg">LOW RISK</span>',
    }
    return badge_map.get(level, f'<span class="badge-unknown">{level}</span>')


def risk_badge_short(level: str) -> str:
    """Compact badge — table use."""
    level = str(level).upper().strip()
    badge_map = {
        "HIGH": '<span class="badge-high">HIGH</span>',
        "MEDIUM": '<span class="badge-medium">MEDIUM</span>',
        "LOW": '<span class="badge-low">LOW</span>',
    }
    return badge_map.get(level, f'<span class="badge-unknown">{level}</span>')


# ═══════════════════════════════════════════════
# DATA ACCESS
# ═══════════════════════════════════════════════

def _load_customer_profiles() -> pd.DataFrame:
    """Load customer static profiles from CSV."""
    if os.path.isfile(CUSTOMERS_CSV):
        try:
            df = pd.read_csv(CUSTOMERS_CSV)
            df["customer_id"] = df["customer_id"].astype(str)
            return df
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()


def fetch_all_customers() -> pd.DataFrame:
    """Fetch all customer profiles from Redis and merge with CSV data."""
    try:
        keys = r.keys("customer:*")
    except Exception:
        return pd.DataFrame()

    if not keys:
        return pd.DataFrame()

    records = []
    for key in keys:
        try:
            profile = r.hgetall(key)
            if not profile:
                continue
            cid = key.replace("customer:", "")
            profile["customer_id"] = cid
            records.append(profile)
        except Exception:
            continue

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    # Ensure numeric columns
    numeric_cols = [
        "txn_count", "total_spend", "withdrawals", "salary_count",
        "essential_spend", "discretionary_spend", "risk_score",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Merge with static profiles
    profiles = _load_customer_profiles()
    if not profiles.empty and "customer_id" in profiles.columns:
        merge_cols = ["customer_id"]
        for c in ["age", "city", "employment_type", "salary", "emi_amount"]:
            if c in profiles.columns:
                merge_cols.append(c)
        df = df.merge(profiles[merge_cols], on="customer_id", how="left")

    return df


def fetch_customer(customer_id) -> dict:
    """Fetch a single customer's full profile from Redis + CSV."""
    key = f"customer:{customer_id}"
    try:
        profile = r.hgetall(key)
    except Exception:
        return {}

    if not profile:
        return {}

    profile["customer_id"] = str(customer_id)

    # Merge static data
    profiles = _load_customer_profiles()
    if not profiles.empty:
        row = profiles[profiles["customer_id"] == str(customer_id)]
        if not row.empty:
            for col in row.columns:
                if col not in profile:
                    profile[col] = str(row.iloc[0][col])

    return profile


def risk_counts(df: pd.DataFrame) -> dict:
    """Count customers by risk level."""
    if df.empty or "risk_level" not in df.columns:
        return {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    counts = df["risk_level"].value_counts().to_dict()
    return {
        "HIGH": counts.get("HIGH", 0),
        "MEDIUM": counts.get("MEDIUM", 0),
        "LOW": counts.get("LOW", 0),
    }


def hardship_distribution(df: pd.DataFrame) -> dict:
    """Count customers by hardship type."""
    if df.empty or "hardship_type" not in df.columns:
        return {}

    dist = df["hardship_type"].value_counts().to_dict()
    dist.pop("NONE", None)
    return dist


# ═══════════════════════════════════════════════
# RISK EXPLAINABILITY
# ═══════════════════════════════════════════════

def get_risk_reasons(profile: dict) -> list:
    """Generate human-readable risk factors from customer data."""
    reasons = []
    salary_count = int(profile.get("salary_count", 0))
    withdrawals = int(profile.get("withdrawals", 0))
    total_spend = float(profile.get("total_spend", 0))
    essential = float(profile.get("essential_spend", 0))
    discretionary = float(profile.get("discretionary_spend", 0))

    if salary_count == 0:
        reasons.append("No recent salary credit detected — possible income disruption")
    if withdrawals > 10:
        reasons.append(f"Abnormally high ATM withdrawals ({withdrawals}) — potential panic liquidity behaviour")
    elif withdrawals > 5:
        reasons.append(f"Elevated cash withdrawals ({withdrawals}) — above normal threshold")
    if total_spend < 2000 and total_spend > 0:
        reasons.append("Spending contraction detected — total expenditure below baseline")
    if essential > 0 and discretionary > 0 and essential > discretionary * 2:
        ratio = round(essential / max(discretionary, 1), 1)
        reasons.append(f"Essential-to-discretionary spend ratio is {ratio}x — financial stress indicator")
    if essential > 0 and discretionary == 0:
        reasons.append("Zero discretionary spending — customer may be in survival mode")

    return reasons


# ═══════════════════════════════════════════════
# INTERVENTION MESSAGES
# ═══════════════════════════════════════════════

def generate_intervention_message(hardship_type: str, customer_id: str) -> str:
    """Generate a professional support message based on hardship classification."""
    messages = {
        "INCOME_SHOCK": (
            f"Dear Valued Customer (ID: {customer_id}),\n\n"
            "We understand that unexpected changes in income can create financial pressure. "
            "As part of our commitment to supporting you through challenging times, "
            "we would like to offer a temporary payment holiday of up to 3 months on your EMI obligations.\n\n"
            "Our dedicated financial support team is available to discuss options that work best for your situation.\n\n"
            "Please contact our support line at 1800-XXX-XXXX or visit your nearest branch.\n\n"
            "Warm regards,\n"
            "Customer Support Division\n"
            "Equilibrate Financial Services"
        ),
        "LIQUIDITY_STRESS": (
            f"Dear Valued Customer (ID: {customer_id}),\n\n"
            "We have identified changes in your account activity and would like to offer our support. "
            "Our complimentary financial wellness programme includes budgeting assistance, "
            "cash flow management tools, and one-on-one sessions with our financial advisors.\n\n"
            "These resources are designed to help you navigate your current financial position with confidence.\n\n"
            "Contact us at 1800-XXX-XXXX to schedule your consultation.\n\n"
            "With care,\n"
            "Customer Support Division\n"
            "Equilibrate Financial Services"
        ),
        "EXPENSE_COMPRESSION": (
            f"Dear Valued Customer (ID: {customer_id}),\n\n"
            "We value your continued relationship with us and have noted recent changes in your spending patterns. "
            "We would like to explore EMI restructuring options that could reduce your monthly repayment burden "
            "while maintaining your account in good standing.\n\n"
            "Our restructuring team can help you find a repayment plan that aligns with your current circumstances.\n\n"
            "Please contact 1800-XXX-XXXX to discuss available options.\n\n"
            "Best regards,\n"
            "Customer Support Division\n"
            "Equilibrate Financial Services"
        ),
    }
    return messages.get(
        hardship_type,
        f"Dear Valued Customer (ID: {customer_id}),\n\n"
        "We are reaching out as part of our proactive customer care programme. "
        "Our support team is available to assist with any financial concerns you may have.\n\n"
        "Contact us at 1800-XXX-XXXX.\n\n"
        "Regards,\n"
        "Customer Support Division\n"
        "Equilibrate Financial Services"
    )
