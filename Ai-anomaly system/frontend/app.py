import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

st.title("🚀 AI Agent-Based Anomaly Detection System")
st.success("System Status: Active Monitoring")

# Generate data
def generate_data():
    # np.random.seed(42)
    data = pd.DataFrame({
        "amount": np.random.normal(1000, 200, 100),
        "time": np.random.randint(1, 24, 100)
    })
    if np.random.rand() > 0.5:
        data.loc[95:, "amount"] = np.random.uniform(3000, 6000, 5)
    else:
        data.loc[95:, "amount"] = np.random.uniform(100, 300, 5)
    return data

# Detection
def detect_anomalies(data):
    model = IsolationForest(contamination=0.05)
    preds = model.fit_predict(data[["amount", "time"]])
    data["anomaly"] = [1 if p == -1 else 0 for p in preds]
    return data

# Explanation
def explain(row):
    if row["amount"] > 4000:
        return "🚨 High transaction, possible fraud"
    elif row["time"] < 5:
        return "⚠️ Unusual transaction time"
    return "Normal"

# Run system
if st.button("Run Detection System"):
    data = generate_data()
    data = detect_anomalies(data)
    data["explanation"] = data.apply(explain, axis=1)

    st.subheader("All Data")
    st.dataframe(data)

    anomalies = data[data["anomaly"] == 1]

    st.subheader("Anomalies")
    st.dataframe(anomalies)

    if not anomalies.empty:
        st.error(f"🚨 ALERT: {len(anomalies)} anomalies detected!")

    st.subheader("Visualization")
    st.scatter_chart(data[["amount", "time"]])
