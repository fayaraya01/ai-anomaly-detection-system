import pandas as pd
import numpy as np

def generate_data():
    np.random.seed(42)
    data = pd.DataFrame({
        "amount": np.random.normal(1000, 200, 100),
        "time": np.random.randint(1, 24, 100)
    })

    # Inject anomalies
    data.loc[95:] = [5000, 2]

    return data