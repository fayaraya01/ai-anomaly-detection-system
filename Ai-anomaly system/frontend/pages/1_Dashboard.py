import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import datetime
import time
# -----------------------------
# 🤖 ADVANCED AI CHATBOT
# -----------------------------
st.subheader("🤖 AI Assistant (Smart Insights)")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# QUICK ACTION BUTTONS (🔥)
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

if col1.button("📊 System Summary"):
    st.session_state.chat_history.append(("AI", f"System processed {len(data)} records with {len(anomalies)} anomalies."))

if col2.button("🚨 Show Top Anomalies"):
    if not anomalies.empty:
        top = anomalies.head(3)
        st.session_state.chat_history.append(("AI", f"Top anomalies:\n{top.to_string(index=False)}"))
    else:
        st.session_state.chat_history.append(("AI", "No anomalies detected."))

if col3.button("⚠️ High Severity Issues"):
    if "amount" in data.columns:
        high = data[data[data.columns[0]] > 4000]
        st.session_state.chat_history.append(("AI", f"{len(high)} high severity issues detected."))
    else:
        st.session_state.chat_history.append(("AI", "No high severity issues."))

if col4.button("🔍 Explain One Anomaly"):
    if not anomalies.empty:
        row = anomalies.iloc[0]
        st.session_state.chat_history.append((
            "AI",
            f"This anomaly occurred due to unusual values: {row.to_dict()}"
        ))
    else:
        st.session_state.chat_history.append(("AI", "No anomalies to explain."))

# -----------------------------
# USER INPUT
# -----------------------------
user_input = st.text_input("Ask about system insights:")

def chatbot_response(text):
    text = text.lower()

    # General
    if "summary" in text:
        return f"Total records: {len(data)}, anomalies: {len(anomalies)}"

    if "anomaly" in text:
        return f"There are {len(anomalies)} anomalies detected."

    # Banking
    if "fraud" in text or "transaction" in text:
        if "amount" in data.columns:
            suspicious = data[data["amount"] > 4000]
            return f"{len(suspicious)} suspicious transactions detected."

    # Cybersecurity
    if "cyber" in text or "attack" in text or "login" in text:
        if "login_attempts" in data.columns:
            attacks = data[data["login_attempts"] > 20]
            return f"{len(attacks)} possible brute-force attacks detected."

    # IoT
    if "iot" in text or "temperature" in text:
        if "temperature" in data.columns:
            issues = data[data["temperature"] > 60]
            return f"{len(issues)} abnormal temperature events detected."

    # Show details
    if "show anomalies" in text:
        if not anomalies.empty:
            return anomalies.head(5).to_string(index=False)
        return "No anomalies detected."

    # Explain
    if "explain" in text:
        if not anomalies.empty:
            row = anomalies.iloc[0]
            return f"Anomaly explanation: {row.to_dict()}"

    return "Try asking about anomalies, fraud, cyber attacks, IoT issues, or summary."

# -----------------------------
# HANDLE INPUT
# -----------------------------
if user_input:
    response = chatbot_response(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("AI", response))

# -----------------------------
# DISPLAY CHAT (CLEAN)
# -----------------------------
for sender, msg in st.session_state.chat_history[-8:]:
    if sender == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 AI:** {msg}")
