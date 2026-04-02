import streamlit as st

st.set_page_config(page_title="AI Monitoring System", layout="wide")

# -----------------------------
# LOGIN SYSTEM
# -----------------------------
def login():
    st.title("🔐 Login to AI Monitoring System")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state["logged_in"] = True
            st.success("Login successful! Redirecting...")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error("Invalid credentials")

# -----------------------------
# SESSION STATE
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# -----------------------------
# LOGIN CHECK
# -----------------------------
if not st.session_state["logged_in"]:
    login()
    st.stop()

# -----------------------------
# HOME PAGE (PRODUCT UI)
# -----------------------------
st.title("🚀 AI Multi-Domain Monitoring Platform")

st.success("🟢 System Active & Secure")

st.markdown("""
## 🔍 About the Product

This is an AI-powered anomaly detection platform designed to monitor and analyze data across multiple domains such as:

- 💳 Banking Systems  
- 🖥️ Cybersecurity Monitoring  
- 🌡️ IoT & Sensor Networks  

---

## ⚙️ What This System Does

- Detects unusual patterns using Machine Learning  
- Explains anomalies in human-readable format  
- Generates real-time alerts  
- Provides analytics and insights  
- Supports multi-domain adaptability  

---

## 🎯 Why This Product is Useful

- Helps detect fraud in financial systems  
- Identifies cyber attacks like brute-force attempts  
- Monitors IoT devices for abnormal behavior  
- Reduces manual monitoring effort  
- Enables faster decision-making  

---

## 🚀 Key Features

- Multi-domain intelligent monitoring  
- Real-time alert system  
- AI-based explanation engine  
- Interactive dashboard  
- Downloadable reports  
""")

# -----------------------------
# QUICK NAVIGATION BUTTON
# -----------------------------
st.warning("⚡ Go to Dashboard to view live system")

if st.button("👉 Open Dashboard"):
    st.switch_page("pages/1_Dashboard.py")
