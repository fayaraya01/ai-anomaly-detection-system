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
        names = ["Arun", "Ravi", "Kumar", "John", "Ali"]

        data = pd.DataFrame({
            "amount": np.random.normal(1000, 200, 100),
            "time": np.random.randint(1, 24, 100),
            "name": np.random.choice(names, 100),
            "account_number": np.random.randint(10000000, 99999999, 100)
        })

        data.loc[95:, "amount"] = np.random.uniform(3000, 6000, 5)
        data.loc[95:, "time"] = np.random.randint(1, 5, 5)

    elif domain == "Cybersecurity":
        users = ["admin", "user1", "guest", "dev", "root"]

        data = pd.DataFrame({
            "login_attempts": np.random.randint(1, 10, 100),
            "failed_attempts": np.random.randint(0, 5, 100),
            "user": np.random.choice(users, 100),
            "time": np.random.randint(1, 24, 100)
        })

        # Inject brute-force attack
        data.loc[95:, "login_attempts"] = np.random.randint(20, 50, 5)
        data.loc[95:, "failed_attempts"] = np.random.randint(15, 40, 5)
        data.loc[95:, "time"] = np.random.randint(1, 5, 5)

    else:  # IoT
        devices = ["Sensor-A", "Sensor-B", "Sensor-C"]
        rooms = ["Living Room", "Kitchen", "Bedroom"]

        data = pd.DataFrame({
            "temperature": np.random.normal(30, 5, 100),
            "time": np.random.randint(1, 24, 100),
            "device": np.random.choice(devices, 100),
            "location": np.random.choice(rooms, 100)
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
        if "login_attempts" in row.index:
            return "🚨 Brute-force attack suspected (multiple failed logins)"
        elif "amount" in row.index and row["amount"] > 4500:
            return "🚨 High-value transaction anomaly"
        elif "temperature" in row.index and row["temperature"] > 60:
            return "🚨 Abnormal temperature spike detected"
        else:
            return "⚠️ Behavioral anomaly detected"
    return "Normal"

def severity(row):
    if row["anomaly"] == 1:
        if "login_attempts" in row.index and row["login_attempts"] > 30:
            return "High"
        elif list(row)[0] > 4000:
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

def human_explanation(row):
    if row["anomaly"] == 1:
        return "This activity is unusual due to abnormal patterns and may require investigation."
    return "This activity appears normal."

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
st.subheader("📈 Activity Visualization")
st.scatter_chart(data, x=data.columns[1], y=data.columns[0])

# -----------------------------
# TIMELINE VIEW (NEW FEATURE)
# -----------------------------
st.subheader("⏳ Attack / Anomaly Timeline")

timeline_data = data.copy()
timeline_data = timeline_data.sort_values(by="time")

st.line_chart(timeline_data.set_index("time")[data.columns[0]])

# -----------------------------
# HUMAN EXPLANATION
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
