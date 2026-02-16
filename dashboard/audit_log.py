"""
Equilibrate Dashboard — Audit Log
Maintains a persistent CSV log of all interventions and actions taken.
"""
import csv
import os
from datetime import datetime

AUDIT_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_log.csv")

AUDIT_FIELDS = ["timestamp", "customer_id", "risk_level", "action_taken", "message_sent"]


def _ensure_log_exists():
    """Create the audit log CSV with headers if it doesn't exist."""
    if not os.path.isfile(AUDIT_LOG_PATH) or os.path.getsize(AUDIT_LOG_PATH) == 0:
        with open(AUDIT_LOG_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=AUDIT_FIELDS)
            writer.writeheader()


def append_audit_log(customer_id: str, risk_level: str, action_taken: str, message_sent: str):
    """Append a new entry to the audit log."""
    _ensure_log_exists()
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "customer_id": customer_id,
        "risk_level": risk_level,
        "action_taken": action_taken,
        "message_sent": message_sent[:200],  # truncate long messages
    }
    with open(AUDIT_LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=AUDIT_FIELDS)
        writer.writerow(row)

    print(f"[AUDIT] {row['timestamp']} | Customer {customer_id} | {action_taken}")
    return row


def read_audit_log():
    """Read the full audit log as a list of dicts."""
    _ensure_log_exists()
    import pandas as pd
    try:
        df = pd.read_csv(AUDIT_LOG_PATH)
        return df
    except Exception:
        return pd.DataFrame(columns=AUDIT_FIELDS)
