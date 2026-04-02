import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="AI Anomaly Detection", layout="wide")

st.title("🚀 AI Agent-Based Anomaly Detection System")
st.success("System Status: Active Monitoring")

# -----------------------------
# Generate Data
# -----------------------------
def generate_data():
    data = pd.DataFrame({
        "amount": np.random.normal(1000, 200, 100),
        "time": np.random.randint(1, 24, 100)
    })

    # Dynamic anomalies
    data.loc[95:, "amount"] = np.random.uniform(3000, 6000, 5)
    data.loc[95:, "time"] = np.random.randint(1, 5, 5)

    return data

# -----------------------------
# Detection
# -----------------------------
def detect_anomalies(data):
    model = IsolationForest(contamination=0.05)
    preds = model.fit_predict(data[["amount", "time"]])
    data["anomaly"] = [1 if p == -1 else 0 for p in preds]
    return data

# -----------------------------
# Explanation + Severity + Score
# -----------------------------
def explain(row):
    if row["anomaly"] == 1:
        if row["amount"] > 4500:
            return "🚨 Critical anomaly: Possible fraud spike"
        elif row["time"] < 5:
            return "⚠️ Suspicious timing detected"
        else:
            return "⚠️ Behavioral anomaly"
    return "Normal"

def severity(row):
    if row["anomaly"] == 1:
        if row["amount"] > 4500:
            return "High"
        elif row["amount"] > 3000:
            return "Medium"
        else:
            return "Low"
    return "None"

def fraud_score(row):
    score = 0
    if row["amount"] > 3000:
        score += 50
    if row["time"] < 5:
        score += 30
    if row["anomaly"] == 1:
        score += 20
    return score

# -----------------------------
# Run System
# -----------------------------
if st.button("Run Detection System"):
    data = generate_data()
    data = detect_anomalies(data)

    data["explanation"] = data.apply(explain, axis=1)
    data["severity"] = data.apply(severity, axis=1)
    data["fraud_score"] = data.apply(fraud_score, axis=1)

    # -----------------------------
    # Summary
    # -----------------------------
    st.subheader("📊 System Summary")

    total = len(data)
    anomalies = len(data[data["anomaly"] == 1])

    col1, col2 = st.columns(2)
    col1.metric("Total Transactions", total)
    col2.metric("Anomalies Detected", anomalies)

    # -----------------------------
    # All Data
    # -----------------------------
    st.subheader("All Transactions")
    st.dataframe(data)

    # -----------------------------
    # Anomalies
    # -----------------------------
    anomalies_df = data[data["anomaly"] == 1]

    st.subheader("🚨 Detected Anomalies")
    st.dataframe(anomalies_df)

    # ALERT
    if not anomalies_df.empty:
        st.error(f"🚨 ALERT: {len(anomalies_df)} anomalies detected!")

    # -----------------------------
    # Visualization
    # -----------------------------
    st.subheader("📈 Visualization")
    st.scatter_chart(data, x="time", y="amount")
