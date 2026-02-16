"""
Risk Engine — Computes risk scores and writes results back to Redis.
Runs continuously, evaluating all customer profiles every 5 seconds.
Stores: risk_level, risk_score, hardship_type, recommended_action
"""
import redis
import time
from datetime import datetime

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

print("=" * 55)
print("  🏦 EQUILIBRATE — Risk Engine v2.0")
print("  Computing risk scores and writing to Redis...")
print("=" * 55)
print()


def calculate_risk(customer_key):
    """Evaluate customer risk and write results back to Redis."""
    data = r.hgetall(customer_key)
    if not data:
        return None

    txn_count = int(data.get("txn_count", 0))
    withdrawals = int(data.get("withdrawals", 0))
    salary_count = int(data.get("salary_count", 0))
    total_spend = float(data.get("total_spend", 0))
    essential = float(data.get("essential_spend", 0))
    discretionary = float(data.get("discretionary_spend", 0))

    risk_score = 0
    hardship_type = "NONE"
    recommended_action = "Continue monitoring"

    # ── Rule 1: No salary credited ──
    if salary_count == 0:
        risk_score += 3
        hardship_type = "INCOME_SHOCK"
        recommended_action = "Offer payment holiday & verify employment"

    # ── Rule 2: High ATM withdrawals ──
    if withdrawals > 10:
        risk_score += 3
        if hardship_type == "NONE":
            hardship_type = "LIQUIDITY_STRESS"
        recommended_action = "Flag for urgent review & suggest digital payments"
    elif withdrawals > 5:
        risk_score += 2
        if hardship_type == "NONE":
            hardship_type = "LIQUIDITY_STRESS"
            recommended_action = "Send financial literacy tips"

    # ── Rule 3: Spending pressure ──
    if essential > 0 and discretionary > 0 and essential > discretionary * 2:
        risk_score += 3
        hardship_type = "EXPENSE_COMPRESSION"
        recommended_action = "Refer to financial counsellor & offer EMI restructuring"
    elif essential > discretionary and essential > 0:
        risk_score += 2
        if hardship_type == "NONE":
            hardship_type = "EXPENSE_COMPRESSION"
            recommended_action = "Send budgeting tips notification"

    # ── Rule 4: Only essential, no discretionary ──
    if essential > 0 and discretionary == 0 and txn_count > 2:
        risk_score += 2
        if hardship_type == "NONE":
            hardship_type = "EXPENSE_COMPRESSION"
            recommended_action = "Offer payment holiday for 1 month"

    # ── Rule 5: High transaction velocity ──
    if txn_count > 50 and total_spend > 10000:
        risk_score += 1

    # ── Classify risk level ──
    if risk_score >= 6:
        risk_level = "HIGH"
    elif risk_score >= 3:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # If LOW risk, clear hardship
    if risk_level == "LOW":
        hardship_type = "NONE"
        recommended_action = "Continue monitoring"

    # ── Write back to Redis ──
    r.hset(customer_key, mapping={
        "risk_level": risk_level,
        "risk_score": str(risk_score),
        "hardship_type": hardship_type,
        "recommended_action": recommended_action,
        "last_risk_eval": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

    return risk_level


# ── Main Loop ──
cycle = 0
while True:
    cycle += 1
    customers = r.keys("customer:*")
    now = datetime.now().strftime("%H:%M:%S")

    high = 0
    medium = 0
    low = 0

    for c in customers:
        level = calculate_risk(c)
        if level == "HIGH":
            high += 1
        elif level == "MEDIUM":
            medium += 1
        else:
            low += 1

    print(f"[{now}] Scan #{cycle} | Customers: {len(customers)} | "
          f"🔴 HIGH: {high} | 🟡 MEDIUM: {medium} | 🟢 LOW: {low}")

    time.sleep(5)
