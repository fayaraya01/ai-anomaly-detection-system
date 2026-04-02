import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import time
import datetime



st.title("📊 Dashboard - Live Monitoring")

# -----------------------------
# SIDEBAR
# -----------------------------
domain = st.sidebar.selectbox(
    "Select Domain",
    ["Banking", "Cybersecurity", "IoT"]
)

# -----------------------------
# DATA GENERATION
# -----------------------------
def generate_data(domain):
    if domain == "Banking":
        data = pd.DataFrame({
            "amount": np.random.normal(1000, 200, 100),
            "time": np.random.randint(1, 24, 100),
            "name": np.random.choice(["Arun","Ravi","Ali"], 100),
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
# EXPLANATION
# -----------------------------
def explain(row):
    if row["anomaly"] == 1:
        return "🚨 Suspicious Activity Detected"
    return "Normal"

# -----------------------------
# RUN
# -----------------------------
data = generate_data(domain)
data = detect(data)
data["explanation"] = data.apply(explain, axis=1)

anomalies = data[data["anomaly"] == 1]

# -----------------------------
# METRICS
# -----------------------------
col1, col2 = st.columns(2)
col1.metric("Total Records", len(data))
col2.metric("Anomalies", len(anomalies))

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
# TABLES
# -----------------------------
st.subheader("📋 Data")
st.dataframe(data)

st.subheader("🚨 Anomalies")
st.dataframe(anomalies)

# -----------------------------
# VISUAL
# -----------------------------
st.subheader("📈 Visualization")
st.line_chart(data[data.columns[0]])
# -----------------------------
# AI CHATBOT (NEW FEATURE)
# -----------------------------
st.subheader("🤖 AI Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask about anomalies or system:")

def chatbot_response(user_input):
    user_input = user_input.lower()

    if "anomaly" in user_input:
        return "Anomalies are unusual patterns detected by the model."
    elif "fraud" in user_input:
        return "High-value or abnormal transactions may indicate fraud."
    elif "cyber" in user_input:
        return "The system detects brute-force attacks using login patterns."
    elif "iot" in user_input:
        return "IoT anomalies include abnormal temperature or sensor values."
    elif "how works" in user_input:
        return "The system uses machine learning to detect deviations and AI logic to explain them."
    else:
        return "I can help explain anomalies, fraud detection, cybersecurity threats, and system behavior."

if user_input:
    response = chatbot_response(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("AI", response))

# Display chat
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.write(f"🧑‍💻 You: {message}")
    else:
        st.write(f"🤖 AI: {message}")
