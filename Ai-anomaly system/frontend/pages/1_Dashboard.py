import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import time
import datetime

# -----------------------------
# 🔐 LOGIN PROTECTION
# -----------------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🔐 Please login first from Home page")
    st.stop()

# -----------------------------
# 🌙 DARK FUTURISTIC UI
# -----------------------------
st.markdown("""
<style>
body, .stApp {background-color:#0E1117;color:#EAEAEA;}
section[data-testid="stSidebar"] {background-color:#111827;}
[data-testid="metric-container"] {
    background-color:#1F2937;
    padding:15px;
    border-radius:10px;
    box-shadow:0 0 10px rgba(0,255,255,0.2);
}
thead tr th {
    background-color:#111827 !important;
    color:#00FFFF !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown("""
<h1 style='color:#00FFFF;text-shadow:0 0 10px #00FFFF;'>
📊 AI Monitoring Dashboard
</h1>
""", unsafe_allow_html=True)

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
        val = row[row.index[0]]
        if val > 4000:
            return "High"
        elif val > 2500:
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
# ⚡ ANIMATED METRICS
# -----------------------------
st.subheader("📊 System Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(data))
col2.metric("Anomalies", len(anomalies))
col3.metric("High Severity", len(data[data["severity"]=="High"]))

# -----------------------------
# 🚨 BLINKING ALERT
# -----------------------------
if not anomalies.empty:
    st.markdown(f"""
    <div style='padding:15px;border-radius:10px;background:#3b0000;
    color:#ff4d4d;font-weight:bold;animation:blinker 1s linear infinite;'>
    🚨 {len(anomalies)} ANOMALIES DETECTED 🚨
    </div>

    <style>
    @keyframes blinker {{
      50% {{ opacity: 0.5; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# HIGHLIGHT ROWS
# -----------------------------
def highlight_rows(row):
    if row["anomaly"] == 1:
        return ['background-color:#3b0000;color:#ff4d4d;font-weight:bold'] * len(row)
    return [''] * len(row)

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📋 Data")
st.dataframe(data.style.apply(highlight_rows, axis=1), use_container_width=True)

# -----------------------------
# 🔍 INVESTIGATION PANEL
# -----------------------------
st.subheader("🔍 Investigate")

if not anomalies.empty:
    anomalies_reset = anomalies.reset_index(drop=True)
    idx = st.selectbox("Select anomaly", anomalies_reset.index)
    st.json(anomalies_reset.loc[idx].to_dict())
else:
    st.info("No anomalies")

# -----------------------------
# 📈 VISUALS
# -----------------------------
st.subheader("📈 Trend")
st.line_chart(data[data.columns[0]])

st.subheader("⏳ Timeline")
timeline = data.sort_values("time")
st.line_chart(timeline.set_index("time")[data.columns[0]])

# -----------------------------
# 🤖 SMART CHATBOT
# -----------------------------
st.subheader("🤖 AI Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask about system:")

def chatbot(text):
    text = text.lower()

    if "summary" in text:
        return f"{len(data)} records, {len(anomalies)} anomalies."

    if "anomaly" in text:
        return f"{len(anomalies)} anomalies detected."

    if "fraud" in text:
        return f"{len(data[data[data.columns[0]]>4000])} suspicious cases."

    if "cyber" in text:
        return f"{len(data[data[data.columns[0]]>20])} possible attacks."

    if "iot" in text:
        return f"{len(data[data[data.columns[0]]>60])} abnormal readings."

    return "Ask about anomalies, fraud, cyber, or summary."

if user_input:
    reply = chatbot(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("AI", reply))

for sender, msg in st.session_state.chat_history[-6:]:
    st.write(f"{'🧑' if sender=='You' else '🤖'} {msg}")

# -----------------------------
# 🔄 AUTO REFRESH
# -----------------------------
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
