import redis
import time

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

print("Alert Engine Started...\n")

def calculate_risk(data):
    txn_count = int(data.get("txn_count", 0))
    withdrawals = int(data.get("withdrawals", 0))
    salary_count = int(data.get("salary_count", 0))
    essential = float(data.get("essential_spend", 0))
    discretionary = float(data.get("discretionary_spend", 0))

    risk = 0

    if salary_count == 0:
        risk += 3
    if withdrawals > 5:
        risk += 2
    if essential > discretionary:
        risk += 2

    if risk >= 5:
        return "HIGH"
    elif risk >= 3:
        return "MEDIUM"
    else:
        return "LOW"


while True:
    customers = r.keys("customer:*")

    for c in customers:
        data = r.hgetall(c)
        level = calculate_risk(data)

        if level == "HIGH":
            print(f"🚨 ALERT: {c} is HIGH RISK — Offer payment holiday")
        elif level == "MEDIUM":
            print(f"⚠️  WARNING: {c} — Send financial advisory SMS")
        else:
            print(f"✅ {c} Healthy")

    print("\nChecking again in 10 seconds...\n")
    time.sleep(10)
