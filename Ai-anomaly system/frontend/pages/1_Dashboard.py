import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import time

# -----------------------------
# LOGIN PROTECTION
# -----------------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🔐 Please login first")
    st.stop()

# -----------------------------
# UI STYLING (PRO LEVEL)
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
}

/* Header */
.header {
    font-size: 28px;
    font-weight: 600;
    color: #f9fafb;
    margin-bottom: 10px;
}

/* Card */
.card {
    background: #111827;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #1f2937;
    margin-bottom: 15px;
}

/* Alert */
.alert {
    background: #3f1d1d;
    padding: 10px;
    border-radius: 10px;
    color: #f87171;
}

/* Table header */
thead tr th {
    background-color: #111827 !important;
    color: #9ca3af !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="header">📊 AI Monitoring Dashboard</div>', unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Controls")

domain = st.sidebar.selectbox("Domain", ["Banking", "Cybersecurity", "IoT"])
auto_refresh = st.sidebar.checkbox("Live Monitoring", value=False)
refresh_rate = st.sidebar.slider("Refresh Rate", 2, 10, 3)

# -----------------------------
# DATA GENERATION
# -----------------------------
def generate_data(domain):
    if domain == "Banking":
        df = pd.DataFrame({
            "amount": np.random.normal(1000, 200, 100),
            "time": np.random.randint(1, 24, 100)
        })
        df.loc[95:, "amount"] = np.random.uniform(3000, 6000, 5)

    elif domain == "Cybersecurity":
        df = pd.DataFrame({
            "login_attempts": np.random.randint(1, 10, 100),
            "failed_attempts": np.random.randint(0, 5, 100)
        })
        df.loc[95:, "login_attempts"] = np.random.randint(20, 50, 5)

    else:
        df = pd.DataFrame({
            "temperature": np.random.normal(30, 5, 100),
            "time": np.random.randint(1, 24, 100)
        })
        df.loc[95:, "temperature"] = np.random.uniform(60, 100, 5)

    return df

# -----------------------------
# DETECTION
# -----------------------------
def detect(df):
    model = IsolationForest(contamination=0.05)
    cols = df.columns[:2]
    df["anomaly"] = model.fit_predict(df[cols])
    df["anomaly"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)
    return df

# -----------------------------
# PROCESS
# -----------------------------
data = detect(generate_data(domain))
anomalies = data[data["anomaly"] == 1]

# -----------------------------
# METRICS (CARD STYLE)
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">Total Records<br><b>{}</b></div>'.format(len(data)), unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">Anomalies<br><b>{}</b></div>'.format(len(anomalies)), unsafe_allow_html=True)

with col3:
    rate = (len(anomalies)/len(data))*100
    st.markdown('<div class="card">Anomaly Rate<br><b>{:.2f}%</b></div>'.format(rate), unsafe_allow_html=True)

# -----------------------------
# ALERT BAR
# -----------------------------
if not anomalies.empty:
    st.markdown(f'<div class="alert">🚨 {len(anomalies)} anomalies detected</div>', unsafe_allow_html=True)
else:
    st.success("System normal")

# -----------------------------
# DATA TABLE
# -----------------------------
st.markdown("### Data Stream")

def highlight(row):
    return ['background-color:#3f1d1d' if row["anomaly"]==1 else '' for _ in row]

st.dataframe(data.style.apply(highlight, axis=1), use_container_width=True)

# -----------------------------
# INVESTIGATION
# -----------------------------
st.markdown("### Investigation")

if not anomalies.empty:
    idx = st.selectbox("Select anomaly", anomalies.index)
    st.json(anomalies.loc[idx].to_dict())
else:
    st.info("No anomalies")

# -----------------------------
# CHART
# -----------------------------
st.markdown("### Trend")
st.line_chart(data[data.columns[0]])

# -----------------------------
# CHATBOT (CLEAN UI)
# -----------------------------
st.markdown("### 🤖 AI Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

query = st.text_input("Ask something")

def respond(q):
    q = q.lower()
    if "summary" in q:
        return f"{len(data)} records, {len(anomalies)} anomalies"
    if "anomaly" in q:
        return f"{len(anomalies)} anomalies detected"
    return "Ask about summary or anomalies"

if query:
    ans = respond(query)
    st.session_state.chat.append(("You", query))
    st.session_state.chat.append(("AI", ans))

for role, msg in st.session_state.chat[-6:]:
    st.markdown(f"**{role}:** {msg}")

# -----------------------------
# AUTO REFRESH
# -----------------------------
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
