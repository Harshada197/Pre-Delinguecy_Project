import pandas as pd
from xgboost import XGBClassifier
import joblib
import os

# resolve paths relative to the project root (one level above /model)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "training_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "ml")
MODEL_PATH = os.path.join(MODEL_DIR, "risk_model.pkl")

print("Loading training data...")

df = pd.read_csv(DATA_PATH)

# features
X = df[["txn_count", "total_amount", "salary_count", "withdrawals"]]

# label
y = df["delinquent"]

print(f"Dataset: {len(df)} rows, {y.sum()} delinquent, {len(df) - y.sum()} non-delinquent")
print("Training XGBoost model...")

model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss"
)

model.fit(X, y)

# create ml/ directory if it doesn't exist
os.makedirs(MODEL_DIR, exist_ok=True)

# save model
joblib.dump(model, MODEL_PATH)

print("Model training complete!")
print(f"Saved as {MODEL_PATH}")
