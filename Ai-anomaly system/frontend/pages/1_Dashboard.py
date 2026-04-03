import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import time

# -----------------------------
# LOGIN PROTECTION
# -----------------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🔐 Please login first from Home page")
    st.stop()

# -----------------------------
# 🎨 PROFESSIONAL DARK UI
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: #e5e7eb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Titles */
h1, h2, h3 {
    color: #f9fafb;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: #111827;
    border: 1px solid #1f2937;
    padding: 15px;
    border-radius: 12px;
}

/* Table */
thead tr th {
    background-color: #111827 !important;
    color: #9ca3af !important;
}

/* Alerts */
.stAlert {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.title("AI Monitoring Dashboard")
st.caption("Real-time anomaly detection across Banking, Cybersecurity, and IoT systems")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Controls")

domain = st.sidebar.selectbox(
    "Domain",
    ["Banking", "Cybersecurity", "IoT"]
)

auto_refresh = st.sidebar.checkbox("Live Monitoring", value=False)
refresh_rate = st.sidebar.slider("Refresh Rate (sec)", 2, 10, 3)

# -----------------------------
# DATA GENERATION
# -----------------------------
def generate_data(domain):
    if domain == "Banking":
        df = pd.DataFrame({
            "amount": np.random.normal(1000, 200, 100),
            "time": np.random.randint(1, 24, 100),
            "user": np.random.choice(["Arun","Ravi","Ali"],100),
        })
        df.loc[95:, "amount"] = np.random.uniform(3000,6000,5)

    elif domain == "Cybersecurity":
        df = pd.DataFrame({
            "login_attempts": np.random.randint(1,10,100),
            "failed_attempts": np.random.randint(0,5,100),
            "time": np.random.randint(1,24,100),
        })
        df.loc[95:, "login_attempts"] = np.random.randint(20,50,5)

    else:
        df = pd.DataFrame({
            "temperature": np.random.normal(30,5,100),
            "time": np.random.randint(1,24,100),
        })
        df.loc[95:, "temperature"] = np.random.uniform(60,100,5)

    return df

# -----------------------------
# DETECTION
# -----------------------------
def detect(df):
    model = IsolationForest(contamination=0.05)
    cols = df.columns[:2]
    preds = model.fit_predict(df[cols])
    df["anomaly"] = [1 if p == -1 else 0 for p in preds]
    return df

# -----------------------------
# PROCESS DATA
# -----------------------------
data = generate_data(domain)
data = detect(data)

anomalies = data[data["anomaly"] == 1]

# -----------------------------
# METRICS
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(data))
col2.metric("Anomalies", len(anomalies))
col3.metric("Anomaly Rate", f"{(len(anomalies)/len(data))*100:.2f}%")

# -----------------------------
# ALERT BAR (CLEAN)
# -----------------------------
if not anomalies.empty:
    st.error(f"{len(anomalies)} anomalies detected")
else:
    st.success("System operating normally")

# -----------------------------
# TABLE (CLEAN)
# -----------------------------
def highlight(row):
    if row["anomaly"] == 1:
        return ["background-color:#3f1d1d"] * len(row)
    return [""] * len(row)

st.subheader("Data Stream")
st.dataframe(data.style.apply(highlight, axis=1), use_container_width=True)

# -----------------------------
# INVESTIGATION PANEL
# -----------------------------
st.subheader("Investigation")

if not anomalies.empty:
    idx = st.selectbox("Select anomaly", anomalies.index)
    st.json(anomalies.loc[idx].to_dict())
else:
    st.info("No anomalies available")

# -----------------------------
# CHARTS
# -----------------------------
st.subheader("Trend")
st.line_chart(data[data.columns[0]])

# -----------------------------
# CHATBOT (CLEAN + USEFUL)
# -----------------------------
st.subheader("AI Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

query = st.text_input("Ask about system")

def respond(q):
    q = q.lower()

    if "summary" in q:
        return f"{len(data)} records, {len(anomalies)} anomalies"

    if "anomaly" in q:
        return f"{len(anomalies)} anomalies detected"

    if "high" in q:
        return f"{len(data[data[data.columns[0]]>4000])} high-value events"

    return "Ask about anomalies, summary, or system status"

if query:
    ans = respond(query)
    st.session_state.chat.append(("You", query))
    st.session_state.chat.append(("AI", ans))

for role, msg in st.session_state.chat[-6:]:
    st.write(f"**{role}:** {msg}")

# -----------------------------
# AUTO REFRESH
# -----------------------------
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
