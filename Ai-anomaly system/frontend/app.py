import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import time

st.set_page_config(page_title="AI Monitoring System", layout="wide")

st.title("🚀 AI Anomaly Detection System")
st.success("🟢 System Status: Live Monitoring")

# -----------------------------
# SIDEBAR (Controls)
# -----------------------------
st.sidebar.header("⚙️ Controls")

auto_refresh = st.sidebar.checkbox("Enable Live Monitoring", value=False)
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 2, 10, 3)

filter_severity = st.sidebar.selectbox(
    "Filter by Severity",
    ["All", "High", "Medium", "Low"]
)

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
# Intelligence Layer
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
# MAIN PIPELINE
# -----------------------------
def run_system():
    data = generate_data()
    data = detect_anomalies(data)

    data["explanation"] = data.apply(explain, axis=1)
    data["severity"] = data.apply(severity, axis=1)
    data["fraud_score"] = data.apply(fraud_score, axis=1)

    return data

# -----------------------------
# EXECUTION
# -----------------------------
data = run_system()

# Apply filter
if filter_severity != "All":
    data = data[data["severity"] == filter_severity]

# -----------------------------
# DASHBOARD METRICS
# -----------------------------
st.subheader("📊 System Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Transactions", len(data))
col2.metric("Anomalies", len(data[data["anomaly"] == 1]))
col3.metric("High Severity", len(data[data["severity"] == "High"]))

# -----------------------------
# ALERT SYSTEM
# -----------------------------
anomalies_df = data[data["anomaly"] == 1]

if not anomalies_df.empty:
    st.error(f"🚨 ALERT: {len(anomalies_df)} anomalies detected!")

# -----------------------------
# DATA DISPLAY
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 All Transactions")
    st.dataframe(data, use_container_width=True)

with col2:
    st.subheader("🚨 Anomalies")
    st.dataframe(anomalies_df, use_container_width=True)

# -----------------------------
# VISUALIZATION
# -----------------------------
st.subheader("📈 Activity Visualization")
st.scatter_chart(data, x="time", y="amount")

# -----------------------------
# AUTO REFRESH (LIVE SYSTEM)
# -----------------------------
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
