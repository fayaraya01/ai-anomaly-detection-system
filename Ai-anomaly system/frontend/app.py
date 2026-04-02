import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="AI Anomaly Detection", layout="wide")

st.title("🚀 AI Agent-Based Anomaly Detection System")
st.success("System Status: Active Monitoring")

# ---------------------------
# Data Generation
# ---------------------------
def generate_data():
    data = pd.DataFrame({
        "amount": np.random.normal(1000, 200, 100),
        "time": np.random.randint(1, 24, 100)
    })

    # Dynamic anomalies
    data.loc[95:, "amount"] = np.random.uniform(3000, 6000, 5)
    data.loc[95:, "time"] = np.random.randint(1, 5, 5)

    return data

# ---------------------------
# Detection
# ---------------------------
def detect_anomalies(data):
    model = IsolationForest(contamination=0.05)
    preds = model.fit_predict(data[["amount", "time"]])
    data["anomaly"] = [1 if p == -1 else 0 for p in preds]
    return data

# ---------------------------
# Explanation + Severity + Score
# ---------------------------
def explain(row):
    if row["amount"] > 5000:
        return "🚨 Extremely high transaction, strong fraud signal"
    elif row["amount"] > 3000:
        return "⚠️ High transaction amount detected"
    elif row["time"] < 5:
        return "⚠️ Activity at unusual hours"
    return "Normal"

def severity(row):
    if row["amount"] > 5000:
        return "High"
    elif row["amount"] > 3000:
        return "Medium"
    elif row["time"] < 5:
        return "Low"
    return "Normal"

def fraud_score(row):
    score = 0
    if row["amount"] > 3000:
        score += 50
    if row["amount"] > 5000:
        score += 30
    if row["time"] < 5:
        score += 20
    return min(score, 100)

# ---------------------------
# RUN SYSTEM
# ---------------------------
if st.button("▶️ Run Detection System"):

    data = generate_data()
    data = detect_anomalies(data)

    data["explanation"] = data.apply(explain, axis=1)
    data["severity"] = data.apply(severity, axis=1)
    data["fraud_score"] = data.apply(fraud_score, axis=1)

    anomalies = data[data["anomaly"] == 1]

    # ---------------------------
    # KPI Metrics
    # ---------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(data))
    col2.metric("Anomalies Detected", len(anomalies))
    col3.metric("Risk %", f"{(len(anomalies)/len(data))*100:.2f}%")

    # ---------------------------
    # Tables
    # ---------------------------
    st.subheader("📋 All Data")
    st.dataframe(data)

    st.subheader("🚨 Anomalies")
    st.dataframe(anomalies)

    # ---------------------------
    # ALERT SYSTEM
    # ---------------------------
    if not anomalies.empty:
        st.error(f"🚨 ALERT: {len(anomalies)} anomalies detected!")

    # ---------------------------
    # FILTER OPTION
    # ---------------------------
    if st.checkbox("Show Only High Severity"):
        st.dataframe(anomalies[anomalies["severity"] == "High"])

    # ---------------------------
    # VISUALIZATION
    # ---------------------------
    st.subheader("📊 Visualization")
    st.scatter_chart(data[["time", "amount"]])
