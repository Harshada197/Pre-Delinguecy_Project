<div align="center">

# ⚡ EQUILIBRATE
### Pre-Delinquency Intervention Engine

**Real-time AI-powered financial distress detection for retail banking**

*Built for the Barclays Hack-O-Hire Hackathon · Team CoreCapital*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white)](https://kafka.apache.org)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![XGBoost](https://img.shields.io/badge/XGBoost-~94%25_Accuracy-brightgreen?style=for-the-badge)](https://xgboost.readthedocs.io)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)

---

> *Equilibrate identifies customers showing early signs of financial distress — **2–4 weeks before a missed payment** — and triggers policy-compliant, personalized interventions that prevent delinquency while preserving customer relationships.*

**[→ GitHub Repository](https://github.com/Harshada197/Pre-Delinquency_Project)**

</div>

---

## 🎯 Problem Statement

Banks typically detect loan delinquency only **after** a customer defaults on an EMI — by which time recovery efforts are costly and customer relationships may already be strained. Most existing collection systems operate reactively, responding only after missed payments occur.

However, early signs of financial distress often appear in customers' **transaction behaviour well before an actual default**. Identifying these early warning signals enables proactive intervention and more effective risk management.

---

## 💡 Solution

A real-time behavioural risk monitoring system that continuously analyzes customer transaction streams and predicts financial distress before delinquency occurs — enabling proactive, personalized intervention.

**Core Pipeline:**
```
Transaction Streams → Behaviour Feature Engine → Risk Prediction Model
    → Explainability (SHAP) → Policy Decision Engine → Bank Dashboard → Customer Intervention
```

**Signals Monitored:** Delayed salary credits · Rising ATM withdrawals / cash hoarding · Reduced discretionary spending · Balance depletion · Late bill payments · Abnormal MCC (Merchant Category Code) spending patterns

---

## 🔄 System Transformation

| ❌ Before Equilibrate | ✅ After Equilibrate |
|---|---|
| Risk detected **after** default patterns appear | **Early risk detection** using behavioural + transactional ML signals |
| Static rule-based alerts with high false positives | Reduced false alerts via **dynamic risk scoring** |
| No real-time transaction-level intelligence | **Real-time risk evaluation** pipeline |
| One-size-fits-all advisory for customers | **Personalized advisory** based on individual financial patterns |
| Limited visibility into intervention ROI | **Measurable ROI** via early intervention analytics |
| Manual monitoring increases operational cost | Automated, scalable cloud-based architecture |

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                               │
│                                                                    │
│    Live Transactions                  Bank Database                │
│    • ATM  • Credit Card               • Account details            │
│    • UPI  • Net Banking               • Loan details               │
└──────────────────┬────────────────────────────┬───────────────────┘
                   │ JSON/AVRO Event Streams     │
┌──────────────────▼────────────────────────────▼───────────────────┐
│                 REAL-TIME EVENT PROCESSING LAYER                   │
│                                                                    │
│  ┌─────────────────┐   ┌──────────────┐   ┌─────────────────────┐ │
│  │  Apache Kafka   │──▶│    Kafka     │──▶│    Apache Flink     │ │
│  │    Clusters     │   │   Connect    │   │                     │ │
│  │                 │   │              │   │ • Tracks windowed   │ │
│  │ • Distributed   │   │ Streams      │   │   patterns          │ │
│  │   immutable logs│   │ historical   │   │ • Maintains stateful│ │
│  │ • Multi-node    │   │ customer     │   │   customer behavior │ │
│  │   replication   │   │ data into    │   │   features in real  │ │
│  │   (zero loss)   │   │ live pipeline│   │   time              │ │
│  └─────────────────┘   └──────────────┘   └──────────┬──────────┘ │
└──────────────────────────────────────────────────────┼────────────┘
                                                        │ Vectorized Behavioral Features
┌───────────────────────────────────────────────────────▼────────────┐
│                    REAL-TIME FEATURE STORE (Redis)                  │
│  • Low-latency lookups to customer profiles                         │
│  • Stores live "state" of customer's financial health (via Flink)   │
└───────────────────────────────────────┬────────────────────────────┘
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────┐
│                   XGBoost MODEL SERVING API                        │
│              Generates a 0–1 Risk Score via REST endpoint          │
│                      Accuracy: ~94%                                │
└──────────────────────────────┬────────────────────────────────────┘
                                │ Risk Score
┌───────────────────────────────▼────────────────────────────────────┐
│                     POLICY & DECISION LAYER                         │
│                                                                     │
│  ┌────────────────┐    ┌───────────────────┐    ┌───────────────┐  │
│  │     SHAP       │───▶│   Policy Engine   │───▶│Case Management│  │
│  │                │    │  (Drools / Pega)  │    │  & Collections│  │
│  │ Interpretable  │    │                   │    │   Workflow    │  │
│  │ risk drivers   │    │ Rule-based        │    │               │  │
│  │ for audit &    │    │ intervention      │    │ Human review, │  │
│  │ compliance     │    │ (Bank Compliance) │    │ approval &    │  │
│  └────────────────┘    └───────────────────┘    │ audit trail   │  │
│                                                  └───────────────┘  │
└──────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────┐
│                      CUSTOMER INTERVENTION                         │
│           SMS Gateway · WhatsApp API · Email · Voice Call          │
│                       Operations Dashboard                         │
└───────────────────────────────┬───────────────────────────────────┘
                                 │ Customer Payment Outcome
                                 └──────── feedback loop ────────▶ Model Retraining
```

---

## ⚙️ Operation Workflow

| Stage | Details |
|---|---|
| **1. Data Ingestion** | Real-time ATM, UPI, and online banking event streams; bridges live telemetry with historical payroll and EMI cycles |
| **2. Behavioural Signal Extraction** | Tracks liquidity erosion, salary drift, and spending shifts; transforms raw events into standardized risk vectors |
| **3. Low-Latency Risk Scoring** | XGBoost predicts default probability 2–4 weeks in advance; segments customers into Low, Medium, and High risk |
| **4. Explainable Risk Attribution** | SHAP isolates specific behaviours driving each risk score; maps AI outputs to transparent, regulatory-compliant labels |
| **5. Policy-Driven Intervention** | Targeted responses deployed based on risk severity; complex cases routed through formal analyst review (human-in-loop) |
| **6. Secure Deployment & Integration** | RESTful API bridges to core banking systems; multi-layer encryption and RBAC for secure, high-scale data handling |

---

## ✨ Key Innovations

| Innovation | Description |
|---|---|
| 🔗 **Policy-Bound Intervention Engine** | Generates rule-based, compliance-approved intervention actions — no manual drafting |
| 🎯 **Personalized Assistance** | Tailors outreach and support actions to individual customer financial patterns and history |
| 🏪 **MCC-Based Spending Detection** | Identifies abnormal spending patterns using Merchant Category Codes across transaction channels |
| 📋 **Operational Priority Queue** | Ranks at-risk customers by urgency score for efficient analyst triage and operations |
| 📈 **ROI Optimization** | Maximizes recovery returns by measuring and learning from intervention outcomes via feedback loop |

---

## 🧠 ML Model — XGBoost Risk Engine

| Attribute | Detail |
|---|---|
| **Model** | XGBoost Classifier (dmlc) |
| **Accuracy** | ~94% |
| **Output** | Continuous risk score (0–1) → HIGH / MEDIUM / LOW |
| **Explainability** | SHAP values for interpretable, audit-ready risk drivers |
| **Serving** | Exposed as REST API endpoint for real-time inference |
| **Feedback Loop** | Customer payment outcomes continuously retrain the model |

### Risk Scoring Signals (0–10 Scale)

| Signal | Max Points | Weight |
|---|---|---|
| Salary gap (no salary + high transaction count) | 3 | 🔴 High |
| ATM withdrawal spike (7-day rolling window) | 2 | 🟡 Medium |
| Spending drop (% change) | 2 | 🟡 Medium |
| Inactivity / survival mode indicator | 1 | 🟢 Low |
| Persona-based supplemental factor | 1 | 🟢 Supplemental |

**Classification:** `HIGH ≥ 5` · `MEDIUM ≥ 3` · `LOW < 3`

---

## 🔬 Hardship Classification

| Type | Trigger Conditions |
|---|---|
| **Income Shock** | No salary credits + ≥5 transactions + INCOME_SHOCK/SILENT_DRAIN persona; OR days since salary >30 + ATM withdrawals ≥3 |
| **Over-Leverage** | Essential spending >70% of total spend + ≥5 transactions |
| **Liquidity Stress** | ATM withdrawals ≥5 + spending drop >20%; OR ATM withdrawals ≥8 |
| **Expense Compression** | Zero discretionary spending + ≥5 transactions; OR spending drop >40% + essential >3× discretionary |
| **Overspending** | Discretionary >2.5× essential + discretionary >₹3,000; OR OVERSPENDER persona + discretionary >2× essential |

---

## 🔐 Security

| Control | Implementation |
|---|---|
| 🛡️ **PII Protection** | Mandatory SHA-256 hashing of all PII at ingestion |
| 🔗 **Encryption in Transit** | End-to-end TLS 1.3 across all internal service communications |
| 📄 **Regulatory Accountability** | Immutable SHAP explainability logs for full audit trail |
| 🔑 **Access Control** | Zero-trust RBAC for all data handling |
| 👤 **Human Governance** | Human-in-the-loop approval before every customer intervention |

---

## ⚠️ Risk Mitigation

**User-Level Risks**

- *Alert fatigue* → Behavioural segmentation + right-time delivery via engagement prediction; context-aware nudges via WhatsApp/SMS
- *Privacy concerns* → Explainable AI with transparent SHAP reasoning; RBI-aligned data handling with minimal exposure
- *Message tone* → Rule-based templates mapped to risk severity; dynamic selection based on repayment history and engagement score

**Model-Level Risks**

- *Over-flagging* → Calibrated probability thresholds using XGBoost scoring; outcome-based feedback loop for continuous precision tuning
- *Missed detections* → Real-time Kafka ingestion with dynamic behavioral features; multi-factor risk scoring across transaction and repayment signals
- *Model drift* → Automated drift detection with periodic retraining pipeline; SHAP monitoring for feature contribution anomalies

**Infrastructure-Level Risks**

- *Delayed intervention* → Event-driven microservices with horizontal scaling; fail-safe retry mechanisms for uninterrupted alert delivery
- *Legacy system integration* → API-based modular design with abstraction gateway layer; plug-and-play deployment without workflow disruption
- *ROI justification* → Early-stage intervention reduces delinquency migration and collection costs; automated targeting improves customer lifetime value

---

## 📊 Dashboard Pages

The Streamlit Operations Dashboard provides a unified view across 5 pages, designed to reduce analyst cognitive load and accelerate intervention times.

**🏠 Operations Hub** — Live KPI cards (total customers, HIGH/MEDIUM/LOW counts), real-time transaction and evaluation timestamps, risk distribution donut chart, and 30-minute trend line.

**📈 Portfolio Overview** — Hardship type × risk level stacked bar charts, risk trends over time, persona distribution breakdown.

**🔴 Risk Queue** — Filterable, sortable table by risk level, hardship type, and customer ID — with recommended actions and Last Updated timestamps, sorted by risk score descending.

**👤 Customer Profile** — Full 360° customer view: demographics, behavioural features, SHAP-driven risk explanation, and transaction pattern analysis.

**📩 Intervention Center** — Select customer → view risk assessment → auto-generate policy-compliant message → review/edit → send via SMS, WhatsApp, or Voice. Full per-customer audit history logged to `data/intervention_log.csv`.

---

## 🗂️ Project Structure

```
Equilibrate/
│
├── kafka/
│   ├── transaction_producer.py       # Persona-driven transaction generator → Kafka
│   └── transactions_consumer.py      # Kafka consumer → data/transactions_raw.csv
│
├── features/
│   ├── feature_engine.py             # Per-transaction feature computation → Redis
│   └── customer_features.py          # Rolling windows, hardship classification, risk scoring
│
├── risk/
│   ├── risk_engine.py                # Continuous re-evaluation loop (every 5 seconds)
│   ├── policy_engine.py              # Policy lookup: hardship × risk → action + message
│   ├── policy_templates.json         # Compliance-approved intervention templates
│   └── alert_engine.py               # Alert generation
│
├── model/
│   ├── build_training_data.py        # Feature aggregation for ML training
│   └── train_model.py                # XGBoost model training & serialization
│
├── storage/
│   └── customer_snapshot_writer.py   # Periodic CSV snapshots of customer state
│
├── dashboard/
│   ├── Home.py                       # Operations Hub
│   ├── utils.py                      # Redis access, CSV merge, sidebar helpers
│   ├── audit_log.py                  # Intervention logging to CSV + Redis
│   ├── styles/theme.css              # Enterprise dark/light CSS theme
│   └── pages/
│       ├── 1_Portfolio_Overview.py
│       ├── 2_Risk_Queue.py
│       ├── 3_Customer_Profile.py
│       └── 4_Intervention_Center.py
│
├── data/
│   ├── customers.csv                 # Static customer master (5,000 records)
│   ├── transactions_raw.csv          # Raw transaction log from Kafka consumer
│   ├── customer_history.csv          # Periodic behavioural snapshots
│   ├── intervention_log.csv          # Full audit trail of all interventions
│   ├── features_dataset.csv          # Aggregated features for ML training
│   └── training_data.csv             # Labeled training dataset
│
├── alert/
│   └── intervention_engine.py        # Intervention dispatch logic
│
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+, Apache Kafka (`C:\kafka`), Redis (`C:\Redis`)

```bash
pip install -r requirements.txt
```

### Launch — Open 7 Terminals in Order

```bash
# Terminal 1 — Redis
C:\Redis\redis-server.exe

# Terminal 2 — Kafka Broker
cd C:\kafka
.\bin\windows\kafka-server-start.bat .\config\server.properties

# Terminal 3 — Transaction Producer
python kafka/transaction_producer.py

# Terminal 4 — Transaction Consumer
python kafka/transactions_consumer.py

# Terminal 5 — Feature Engine
python features/feature_engine.py

# Terminal 6 — Risk Engine
python risk/risk_engine.py

# Terminal 7 — Dashboard
streamlit run dashboard/Home.py
```

> **Kafka topic setup (if needed):**
> ```bash
> .\bin\windows\kafka-topics.bat --create --topic transactions --bootstrap-server 127.0.0.1:9092 --partitions 1 --replication-factor 1
> ```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Stream Ingestion | Apache Kafka, Kafka Connect |
| Stream Processing | Apache Flink |
| Feature Store | Redis |
| ML Model | XGBoost (dmlc), scikit-learn, MLflow |
| Explainability | SHAP |
| Dashboard | Streamlit + Plotly |
| Notifications | Gupshup (SMS / WhatsApp / Voice) |
| API | REST |
| Data Processing | Pandas |

---

## 🔭 Future Scope

| Phase | Enhancement |
|---|---|
| **Deep Learning** | LSTM/Transformer models for sequential spending pattern analysis |
| **Cross-Channel Behaviour** | Combines ATM, UPI, and online data streams for richer predictions |
| **Fraud & Stress Integration** | Integrates stress analysis with fraud detection signals |
| **Cloud-Native Deployment** | Kubernetes / SageMaker for large-scale production hosting |
| **Explainable AI v2** | Enhanced SHAP + rule explanations tailored for regulators |
| **Multi-Product Growth** | Expand coverage to credit cards, personal loans, and savings products |

---

## 📈 Impact & Benefits

The system identifies customers **2–4 weeks before potential default** and triggers supportive interventions — flexible repayment, financial counselling, or payment holiday — preventing delinquency while preserving relationships.

**For the Bank:** Reduction in NPAs and bad loans · Lower recovery and collection costs · Smarter, data-driven lending decisions · Healthier overall loan portfolio · Better customer lifetime value and retention.

---

## 📚 References

[1] Y. Zhang, J. Chen, and L. Wang, "Predicting mortgage early delinquency with machine learning methods," *Eur. J. Oper. Res.*, vol. 291, no. 3, pp. 927–946, Mar. 2021.

[2] J. K. Mwangi and P. N. Otieno, "A model for predicting pre-delinquency of credit card accounts using ensemble machine learning," Strathmore Univ. Research Repository, 2023.

[3] S. Lessmann, W. H. Cao, and X. H. Shi, "Predicting consumer default: A deep learning approach," NBER Working Paper no. 26165, 2019.

[4] S. S. K. Reddy, V. K. Reddy, and P. R. Kumar, "Machine learning and deep learning for loan prediction in banking," in *Proc. IEEE ICICCT*, Apr. 2024, pp. 1–6.

[5] A. Bastos and J. Matos, "Predicting delinquency on mortgage loans: An exhaustive machine learning approach," *Int. J. Ind. Eng. Manag.*, vol. 12, no. 2, pp. 107–116, 2021.

---

## 👥 Team CoreCapital

| Member |
|---|
| Harshada Dhas |
| Anushree Surve |
| Srushti Kotgire |
| Zahara Bhori |
| Kasturi Deo |

---

<div align="center">

**Built with ❤️ for Barclays Hack-O-Hire**

*Catch financial distress early. Intervene intelligently. Protect customers proactively.*

</div>
