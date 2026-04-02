import streamlit as st
import pandas as pd
import numpy as np

st.title("📈 Analytics")

data = pd.DataFrame({
    "time": np.arange(50),
    "anomalies": np.random.randint(0,10,50)
})

st.line_chart(data.set_index("time"))

st.bar_chart(pd.DataFrame({
    "severity": ["High","Medium","Low"],
    "count": [5,10,20]
}).set_index("severity"))
