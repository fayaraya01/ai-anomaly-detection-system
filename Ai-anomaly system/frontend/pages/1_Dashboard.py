import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import datetime
import time

# -----------------------------
# LOGIN PROTECTION
# -----------------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🔐 Please login first from Home page")
    st.stop()

# -----------------------------
# PAGE TITLE
# -----------------------------
st.title("📊 Dashboard - Live Monitoring")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("⚙️ Controls")

domain = st.sidebar.selectbox(
    "Select Domain",
    ["Banking", "Cybersecurity", "IoT"]
)

auto_refresh = st.sidebar.checkbox("Enable Live Monitoring", value=False)
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 2, 10, 3)

# -----------------------------
# DATA GENERATION
# -----------------------------
def generate_data(domain):
    if domain == "Banking":
        data = pd.DataFrame({
            "amount": np.random.normal(1000, 200, 100),
            "time": np.random.randint(1, 24, 100),
            "name": np.random.choice(["Arun","Ravi","Ali"],100),
            "account": np.random.randint(10000000,99999999,100)
        })
        data.loc[95:, "amount"] = np.random.uniform(3000,6000,5)

    elif domain == "Cybersecurity":
        data = pd.DataFrame({
            "login_attempts": np.random.randint(1,10,100),
            "failed_attempts": np.random.randint(0,5,100),
            "user": np.random.choice(["admin","guest","dev"],100),
            "time": np.random.randint(1,24,100)
        })
        data.loc[95:, "login_attempts"] = np.random.randint(20,50,5)
        data.loc[95:, "failed_attempts"] = np.random.randint(15,40,5)

    else:
        data = pd.DataFrame({
            "temperature": np.random.normal(30,5,100),
            "time": np.random.randint(1,24,100),
            "device": np.random.choice(["Sensor-A","Sensor-B"],100),
            "room": np.random.choice(["Hall","Kitchen"],100)
        })
        data.loc[95:, "temperature"] = np.random.uniform(60,100,5)

    return data

# -----------------------------
# DETECTION
# -----------------------------
def detect(data):
    model = IsolationForest(contamination=0.05)
    cols = data.columns[:2]
    preds = model.fit_predict(data[cols])
    data["anomaly"] = [1 if p == -1 else 0 for p in preds]
    return data

# -----------------------------
# SEVERITY
# -----------------------------
def get_severity(row):
    if row["anomaly"] == 1:
        if row[data.columns[0]] > 4000:
            return "High"
        elif row[data.columns[0]] > 2500:
            return "Medium"
        else:
            return "Low"
    return "Normal"

# -----------------------------
# EXPLANATION
# -----------------------------
def explain(row):
    if row["anomaly"] == 1:
        if "login_attempts" in row.index:
            return "🚨 Brute-force attack suspected"
        elif "amount" in row.index:
            return "🚨 Suspicious transaction"
        elif "temperature" in row.index:
            return "🚨 Abnormal sensor reading"
        return "⚠️ Behavioral anomaly"
    return "Normal"

# -----------------------------
# RUN SYSTEM
# -----------------------------
data = generate_data(domain)
data = detect(data)

data["severity"] = data.apply(get_severity, axis=1)
data["explanation"] = data.apply(explain, axis=1)

anomalies = data[data["anomaly"] == 1]

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(data))
col2.metric("Anomalies", len(anomalies))
col3.metric("High Severity", len(data[data["severity"]=="High"]))

# -----------------------------
# ALERT PANEL
# -----------------------------
st.subheader("🔔 Alerts")

if not anomalies.empty:
    st.error(f"🚨 {len(anomalies)} anomalies detected!")
    for _, row in anomalies.head(3).iterrows():
        st.warning(f"{row['explanation']} | Severity: {row['severity']}")
else:
    st.success("System Normal")

# -----------------------------
# HIGHLIGHT FUNCTION
# -----------------------------
def highlight_rows(row):
    if row["anomaly"] == 1:
        return ['background-color: #ffcccc'] * len(row)
    return [''] * len(row)

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📋 All Data")
st.dataframe(data.style.apply(highlight_rows, axis=1), use_container_width=True)

# -----------------------------
# INVESTIGATION PANEL
# -----------------------------
st.subheader("🔍 Investigate Anomaly")

if not anomalies.empty:
    anomalies_reset = anomalies.reset_index(drop=True)

    idx = st.selectbox("Select anomaly", anomalies_reset.index)
    selected = anomalies_reset.loc[idx]

    st.error(f"⚠️ Selected Anomaly #{idx}")
    st.json(selected.to_dict())
else:
    st.info("No anomalies to investigate")

# -----------------------------
# VISUALIZATION
# -----------------------------
st.subheader("📈 Trend")
st.line_chart(data[data.columns[0]])

# -----------------------------
# CHATBOT (AFTER DATA ✔️)
# -----------------------------
st.subheader("🤖 AI Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask about system:")

def chatbot(text):
    text = text.lower()

    if "summary" in text:
        return f"{len(data)} records processed, {len(anomalies)} anomalies found."

    if "anomaly" in text:
        return f"There are {len(anomalies)} anomalies currently."

    if "fraud" in text:
        return f"{len(data[data[data.columns[0]]>4000])} suspicious cases detected."

    if "cyber" in text:
        return f"{len(data[data[data.columns[0]]>20])} possible attacks detected."

    if "iot" in text:
        return f"{len(data[data[data.columns[0]]>60])} abnormal readings detected."

    return "Ask about anomalies, fraud, cyber attacks, or system summary."

if user_input:
    reply = chatbot(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("AI", reply))

for sender, msg in st.session_state.chat_history[-6:]:
    st.write(f"{'🧑' if sender=='You' else '🤖'} {msg}")

# -----------------------------
# AUTO REFRESH
# -----------------------------
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
