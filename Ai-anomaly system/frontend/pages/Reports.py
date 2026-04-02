import streamlit as st
import pandas as pd

st.title("📄 Reports")

data = pd.DataFrame({
    "event": ["Anomaly","Normal","Anomaly"],
    "severity": ["High","Low","Medium"]
})

st.dataframe(data)

csv = data.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Report",
    csv,
    "report.csv",
    "text/csv"
)
