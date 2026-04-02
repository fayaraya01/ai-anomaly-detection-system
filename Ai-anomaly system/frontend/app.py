import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import time

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Monitoring System", layout="wide")

st.title("🚀 AI Multi-Domain Anomaly Detection System")
st.success("🟢 System Status: Live Monitoring")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("⚙️ Controls")

domain = st.sidebar.selectbox(
    "Select Data Domain",
    ["Banking", "Cybersecurity", "IoT"]
)

auto_refresh = st.sidebar.checkbox("Enable Live Monitoring", value=False)
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 2, 10, 3)

filter_severity = st.sidebar.selectbox(
    "Filter by Severity",
    ["All", "High", "Medium", "Low"]
)

# -----------------------------
# DATA GENERATION
# -----------------------------
def generate_data(domain):
    if domain == "Banking":
        data = pd.DataFrame({
            "amount": np.random.normal(1000, 200, 100),
            "time": np.random.randint(1, 24, 100)
        })
        data.loc[95:, "amount"] = np.random.uniform(3000, 6000, 5)
        data.loc[95:, "time"] = np.random.randint(1, 5, 5)

    elif domain == "Cybersecurity":
        data = pd.DataFrame({
            "data_transfer": np.random.normal(500, 100, 100),
            "access_time": np.random.randint(1, 24, 100)
        })
        data.loc[95:, "data_transfer"] = np.random.uniform(2000, 5000, 5)
        data.loc[95:, "access_time"] = np.random.randint(1, 5, 5)

    else:  # IoT
        data = pd.DataFrame({
            "temperature": np.random.normal(30, 5, 100),
            "time": np.random.randint(1, 24, 100)
        })
        data.loc[95:, "temperature"] = np.random.uniform(60, 100, 5)
        data.loc[95:, "time"] = np.random.randint(1, 5, 5)

    return data

# -----------------------------
# DETECTION
# -----------------------------
def detect_anomalies(data):
    model = IsolationForest(contamination=0.05)
    cols = data.columns[:2]
    preds = model.fit_predict(data[cols])
    data["anomaly"] = [1 if p == -1 else 0 for p in preds]
    return data

# -----------------------------
# INTELLIGENCE
# -----------------------------
def explain(row):
    if row["anomaly"] == 1:
        if list(row)[0] > 4500:
            return "🚨 Critical anomaly detected"
        elif list(row)[1] < 5:
            return "⚠️ Suspicious behavior detected"
        else:
            return "⚠️ Pattern deviation"
    return "Normal"

def severity(row):
    if row["anomaly"] == 1:
        if list(row)[0] > 4500:
            return "High"
        elif list(row)[0] > 3000:
            return "Medium"
        else:
            return "Low"
    return "None"

def fraud_score(row):
    score = 0
    if list(row)[0] > 3000:
        score += 50
    if list(row)[1] < 5:
        score += 30
    if row["anomaly"] == 1:
        score += 20
    return score

# -----------------------------
# HUMAN EXPLANATION
# -----------------------------
def human_explanation(row):
    if row["anomaly"] == 1:
        return f"This record looks unusual because the value is high and occurs at an uncommon time, which may indicate abnormal system behavior."
    return "This record follows normal expected patterns."

# -----------------------------
# RUN SYSTEM
# -----------------------------
def run_system(domain):
    data = generate_data(domain)
    data = detect_anomalies(data)

    data["explanation"] = data.apply(explain, axis=1)
    data["severity"] = data.apply(severity, axis=1)
    data["fraud_score"] = data.apply(fraud_score, axis=1)
    data["human_explanation"] = data.apply(human_explanation, axis=1)

    return data

# -----------------------------
# EXECUTION
# -----------------------------
data = run_system(domain)

if filter_severity != "All":
    data = data[data["severity"] == filter_severity]

st.subheader(f"📊 Domain: {domain} Monitoring")

# -----------------------------
# METRICS
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(data))
col2.metric("Anomalies", len(data[data["anomaly"] == 1]))
col3.metric("High Severity", len(data[data["severity"] == "High"]))

# -----------------------------
# ALERT
# -----------------------------
anomalies_df = data[data["anomaly"] == 1]

if not anomalies_df.empty:
    st.error(f"🚨 ALERT: {len(anomalies_df)} anomalies detected!")

# -----------------------------
# DATA DISPLAY
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 All Data")
    st.dataframe(data, use_container_width=True)

with col2:
    st.subheader("🚨 Anomalies")
    st.dataframe(anomalies_df, use_container_width=True)

# -----------------------------
# VISUALIZATION
# -----------------------------
st.subheader("📈 Visualization")
st.scatter_chart(data, x=data.columns[1], y=data.columns[0])

# -----------------------------
# HUMAN EXPLANATION VIEW
# -----------------------------
st.subheader("🧠 Explain Like Human")

if st.button("Explain First Anomaly"):
    if not anomalies_df.empty:
        st.info(anomalies_df.iloc[0]["human_explanation"])

# -----------------------------
# DOWNLOAD
# -----------------------------
st.subheader("📥 Download Report")

csv = data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="anomaly_report.csv",
    mime="text/csv"
)

# -----------------------------
# AUTO REFRESH
# -----------------------------
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
