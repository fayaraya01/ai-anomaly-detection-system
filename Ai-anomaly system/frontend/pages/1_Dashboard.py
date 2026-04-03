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
# SIDEBAR CONTROLS
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
            "name": np.random.choice(["Arun", "Ravi", "Ali"], 100),
            "account_number": np.random.randint(10000000, 99999999, 100)
        })
        data.loc[95:, "amount"] = np.random.uniform(3000, 6000, 5)
        data.loc[95:, "time"] = np.random.randint(1, 5, 5)

    elif domain == "Cybersecurity":
        data = pd.DataFrame({
            "login_attempts": np.random.randint(1, 10, 100),
            "failed_attempts": np.random.randint(0, 5, 100),
            "user": np.random.choice(["admin", "guest", "dev"], 100),
            "time": np.random.randint(1, 24, 100)
        })
        data.loc[95:, "login_attempts"] = np.random.randint(20, 50, 5)
        data.loc[95:, "failed_attempts"] = np.random.randint(15, 40, 5)
        data.loc[95:, "time"] = np.random.randint(1, 5, 5)

    else:  # IoT
        data = pd.DataFrame({
            "temperature": np.random.normal(30, 5, 100),
            "time": np.random.randint(1, 24, 100),
            "device": np.random.choice(["Sensor-A", "Sensor-B"], 100),
            "room": np.random.choice(["Hall", "Kitchen"], 100)
        })
        data.loc[95:, "temperature"] = np.random.uniform(60, 100, 5)
        data.loc[95:, "time"] = np.random.randint(1, 5, 5)

    return data

# -----------------------------
# ANOMALY DETECTION
# -----------------------------
def detect(data):
    model = IsolationForest(contamination=0.05)
    cols = data.columns[:2]
    preds = model.fit_predict(data[cols])
    data["anomaly"] = [1 if p == -1 else 0 for p in preds]
    return data

# -----------------------------
# EXPLANATION
# -----------------------------
def explain(row):
    if row["anomaly"] == 1:
        if "login_attempts" in row.index:
            return "🚨 Possible brute-force attack"
        elif "amount" in row.index and row["amount"] > 4000:
            return "🚨 High-value suspicious transaction"
        elif "temperature" in row.index and row["temperature"] > 60:
            return "🚨 Abnormal temperature spike"
        else:
            return "⚠️ Behavioral anomaly"
    return "Normal"

# -----------------------------
# RUN SYSTEM
# -----------------------------
data = generate_data(domain)
data = detect(data)
data["explanation"] = data.apply(explain, axis=1)

anomalies = data[data["anomaly"] == 1]

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📊 System Overview")

col1, col2 = st.columns(2)
col1.metric("Total Records", len(data))
col2.metric("Anomalies Detected", len(anomalies))

# -----------------------------
# ALERT PANEL
# -----------------------------
st.subheader("🔔 Real-Time Alerts")

if not anomalies.empty:
    for _, row in anomalies.head(5).iterrows():
        st.warning(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {row['explanation']}")
else:
    st.success("No anomalies detected")

# -----------------------------
# DATA TABLES
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 All Data")
    st.dataframe(data, use_container_width=True)

with col2:
    st.subheader("🚨 Anomalies")
    st.dataframe(anomalies, use_container_width=True)

# -----------------------------
# VISUALIZATION
# -----------------------------
st.subheader("📈 Activity Visualization")
st.line_chart(data[data.columns[0]])

# -----------------------------
# TIMELINE VIEW
# -----------------------------
st.subheader("⏳ Anomaly Timeline")

timeline = data.sort_values("time")
st.line_chart(timeline.set_index("time")[data.columns[0]])

# -----------------------------
# AI CHATBOT (IMPROVED)
# -----------------------------
st.subheader("🤖 AI Assistant")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input
user_input = st.text_input("Ask something about system:")

def chatbot_response(text, anomalies):
    text = text.lower()

    if "anomaly" in text:
        return f"There are currently {len(anomalies)} anomalies detected in the system."

    elif "fraud" in text:
        if "amount" in data.columns:
            high = data[data["amount"] > 4000]
            return f"{len(high)} high-value suspicious transactions detected."

    elif "cyber" in text or "attack" in text:
        if "login_attempts" in data.columns:
            attacks = data[data["login_attempts"] > 20]
            return f"{len(attacks)} possible brute-force attacks detected."

    elif "iot" in text or "temperature" in text:
        if "temperature" in data.columns:
            high_temp = data[data["temperature"] > 60]
            return f"{len(high_temp)} abnormal temperature events detected."

    elif "summary" in text:
        return f"System processed {len(data)} records with {len(anomalies)} anomalies."

    else:
        return "Try asking about anomalies, fraud, cyber attacks, or system summary."

# Process only once per input
if user_input:
    response = chatbot_response(user_input, anomalies)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("AI", response))

# Show only last 6 messages (clean UI)
for sender, msg in st.session_state.chat_history[-6:]:
    if sender == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 AI:** {msg}")

# -----------------------------
# AUTO REFRESH
# -----------------------------
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
