import streamlit as st
import requests
import pandas as pd

st.title("🚀 AI Agent-Based Anomaly Detection System")


if st.button("Run Detection System"):
    try:
        requests.get("http://127.0.0.1:8000/run")
        st.success("System executed successfully!")
    except:
        st.error("Backend not running!")

response = requests.get("http://127.0.0.1:8000/data")

data = pd.DataFrame(response.json())

if not data.empty:
    st.subheader("All Data")
    st.dataframe(data)

    st.subheader("Anomalies")
    st.dataframe(data[data["anomaly"] == 1])

    st.subheader("Visualization")
    st.scatter_chart(data[["amount", "time"]])
st.subheader("📊 Summary")

total = len(data)
anomalies = len(data[data["anomaly"] == 1])

st.write(f"Total Transactions: {total}")
st.write(f"Anomalies Detected: {anomalies}")
st.subheader("Anomalies")
st.dataframe(data[data["anomaly"] == 1])
st.subheader("Anomalies")
anomalies = data[data["anomaly"] == 1]
st.dataframe(anomalies)

# 🚨 ALERT SYSTEM (ADD HERE)
if not anomalies.empty:
    st.error("🚨 ALERT: Anomalies Detected!")
import time

if st.button("Start Live Monitoring"):
    for i in range(5):
        requests.get("http://127.0.0.1:8000/run")
        st.write(f"Run {i+1} completed")
        time.sleep(2)
if not anomalies.empty:
    st.error(f"🚨 ALERT: {len(anomalies)} anomalies detected!")