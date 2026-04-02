import streamlit as st

st.set_page_config(page_title="AI Monitoring System", layout="wide")

# -----------------------------
# SIMPLE LOGIN SYSTEM
# -----------------------------
def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid credentials")

# -----------------------------
# SESSION CHECK
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# -----------------------------
# MAIN PAGE
# -----------------------------
st.title("🚀 AI Multi-Domain Monitoring System")

st.success("🟢 Logged in successfully")

st.markdown("""
Use the sidebar to navigate:

- 📊 Dashboard  
- 📈 Analytics  
- 📄 Reports  
""")
