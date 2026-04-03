import streamlit as st

st.set_page_config(page_title="AI Monitoring System", layout="wide")

# -----------------------------
# SESSION INIT
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# -----------------------------
# LOGIN FUNCTION
# -----------------------------
def login():
    st.title("🔐 Login to AI Monitoring System")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state["logged_in"] = True
            st.success("Login successful! Use sidebar to open Dashboard.")
        else:
            st.error("Invalid credentials")

# -----------------------------
# LOGIN CHECK
# -----------------------------
if not st.session_state["logged_in"]:
    login()
    st.stop()

# -----------------------------
# HOME PAGE
# -----------------------------
st.title("🚀 AI Multi-Domain Monitoring Platform")
st.success("🟢 System Active & Secure")

st.markdown("""
## 🔍 About the Product

This AI-powered system detects anomalies across:

- 💳 Banking  
- 🖥️ Cybersecurity  
- 🌡️ IoT Systems  

---

## ⚙️ Features

- Real-time anomaly detection  
- AI-based explanations  
- Alert system  
- Interactive dashboard  
- Multi-domain adaptability  

---

👉 Use the sidebar to navigate:
- 📊 Dashboard  
- 📈 Analytics  
- 📄 Reports  
""")

st.warning("⚡ Go to Dashboard to view live system")
