import redis
import time
from datetime import datetime

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

print("=" * 60)
print("   🏦 PRE-DELINQUENCY INTERVENTION ENGINE")
print("   Monitoring customer risk in real-time...")
print("=" * 60)
print()

def analyze_risk(profile):
    """Analyze risk with detailed reasons and data points"""
    txn_count = int(profile.get("txn_count", 0))
    withdrawals = int(profile.get("withdrawals", 0))
    salary_count = int(profile.get("salary_count", 0))
    total_spend = float(profile.get("total_spend", 0))
    essential = float(profile.get("essential_spend", 0))
    discretionary = float(profile.get("discretionary_spend", 0))
    last_salary = profile.get("last_salary_ts", "")

    risk_score = 0
    reasons = []
    interventions = []

    # ── Rule 1: No salary received ──
    if salary_count == 0:
        risk_score += 3
        reasons.append("❌ No salary credited yet — possible job loss or delayed payment")
        interventions.append("📞 Contact customer to verify employment status")
        interventions.append("📋 Offer EMI restructuring plan")
    elif salary_count == 1 and txn_count > 20:
        reasons.append("⚠️ Only 1 salary in many transactions — irregular income pattern")
        risk_score += 1
        interventions.append("📊 Monitor salary frequency over next 30 days")

    # ── Rule 2: High ATM withdrawals ──
    if withdrawals > 10:
        risk_score += 3
        reasons.append(f"🏧 Very high cash withdrawals: {withdrawals} times — panic withdrawal pattern")
        interventions.append("🚨 Flag for urgent manual review")
        interventions.append("💳 Suggest digital payment alternatives")
    elif withdrawals > 5:
        risk_score += 2
        reasons.append(f"🏧 High ATM withdrawals: {withdrawals} times — above normal threshold (5)")
        interventions.append("📱 Send financial literacy tips via SMS")

    # ── Rule 3: Essential > Discretionary spending ──
    if essential > 0 and discretionary > 0:
        if essential > discretionary * 2:
            risk_score += 3
            ratio = round(essential / max(discretionary, 1), 1)
            reasons.append(f"💸 Severe financial stress — essential spending {ratio}x higher than discretionary")
            reasons.append(f"   Essential: ₹{essential:.0f} | Discretionary: ₹{discretionary:.0f}")
            interventions.append("🏥 Refer to financial counsellor immediately")
            interventions.append("💰 Offer emergency microloan at reduced rate")
        elif essential > discretionary:
            risk_score += 2
            reasons.append(f"💰 Financial pressure — essential (₹{essential:.0f}) > discretionary (₹{discretionary:.0f})")
            interventions.append("📩 Send budgeting tips notification")
    elif essential > 0 and discretionary == 0:
        risk_score += 2
        reasons.append(f"💸 Only essential spending (₹{essential:.0f}), zero discretionary — survival mode")
        interventions.append("🤝 Offer payment holiday for 1 month")

    # ── Rule 4: Very high spend velocity ──
    if txn_count > 50 and total_spend > 10000:
        risk_score += 1
        reasons.append(f"📈 High transaction velocity: {txn_count} transactions, ₹{total_spend:.0f} total spend")
        interventions.append("📊 Activate spending limit alerts")

    # ── Rule 5: Low activity (may indicate account abandonment) ──
    if txn_count <= 2 and salary_count == 0:
        reasons.append(f"🔇 Very low activity ({txn_count} txns) with no salary — possible account abandonment")
        interventions.append("📧 Send re-engagement notification")

    # ── Classify risk level ──
    if risk_score >= 6:
        level = "🔴 CRITICAL"
    elif risk_score >= 4:
        level = "🟠 HIGH"
    elif risk_score >= 2:
        level = "🟡 MEDIUM"
    else:
        level = "🟢 LOW"

    return {
        "level": level,
        "score": risk_score,
        "reasons": reasons,
        "interventions": interventions,
        "data": {
            "txn_count": txn_count,
            "withdrawals": withdrawals,
            "salary_count": salary_count,
            "total_spend": total_spend,
            "essential_spend": essential,
            "discretionary_spend": discretionary,
            "last_salary_ts": last_salary
        }
    }


cycle = 0

while True:
    cycle += 1
    customers = r.keys("customer:*")
    now = datetime.now().strftime("%H:%M:%S")

    critical_count = 0
    high_count = 0
    medium_count = 0
    low_count = 0

    print(f"\n{'=' * 60}")
    print(f"   📊 SCAN #{cycle} | Time: {now} | Customers: {len(customers)}")
    print(f"{'=' * 60}")

    for cust in customers:
        profile = r.hgetall(cust)
        if not profile:
            continue

        result = analyze_risk(profile)
        level = result["level"]
        score = result["score"]
        reasons = result["reasons"]
        interventions = result["interventions"]
        data = result["data"]

        # Count by category
        if "CRITICAL" in level:
            critical_count += 1
        elif "HIGH" in level:
            high_count += 1
        elif "MEDIUM" in level:
            medium_count += 1
        else:
            low_count += 1

        # Only print details for non-LOW risk customers
        if score >= 2:
            print(f"\n  ┌─── {level} | {cust} | Risk Score: {score}/8")
            print(f"  │ Transactions: {data['txn_count']} | Withdrawals: {data['withdrawals']} | Salary Credits: {data['salary_count']}")
            print(f"  │ Total Spend: ₹{data['total_spend']:.0f} | Essential: ₹{data['essential_spend']:.0f} | Discretionary: ₹{data['discretionary_spend']:.0f}")

            if data['last_salary_ts']:
                print(f"  │ Last Salary: {data['last_salary_ts']}")

            print(f"  │")
            print(f"  │ 📋 RISK FACTORS:")
            for reason in reasons:
                print(f"  │   {reason}")

            print(f"  │")
            print(f"  │ 🎯 RECOMMENDED ACTIONS:")
            for action in interventions:
                print(f"  │   {action}")

            print(f"  └{'─' * 55}")

    # Summary dashboard
    print(f"\n  ╔{'═' * 40}╗")
    print(f"  ║  🔴 CRITICAL: {critical_count:>4}  │  🟠 HIGH: {high_count:>4}  ║")
    print(f"  ║  🟡 MEDIUM:  {medium_count:>4}  │  🟢 LOW:  {low_count:>4}  ║")
    print(f"  ╚{'═' * 40}╝")

    time.sleep(10)
