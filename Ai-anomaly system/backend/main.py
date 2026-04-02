from fastapi import FastAPI
import pandas as pd

from backend.model import DetectionAgent
from backend.agents import ExplanationAgent
from data.generator import generate_data
from database.db import database

app = FastAPI()

detector = DetectionAgent()
explainer = ExplanationAgent()

@app.get("/run")
def run_pipeline():
    data = generate_data()

    anomalies = detector.detect(data)
    data["anomaly"] = anomalies

    results = []

    for _, row in data.iterrows():
        row_dict = row.to_dict()

        if row_dict["anomaly"] == 1:
            explanation = explainer.explain(row_dict)
        else:
            explanation = "Normal"

        row_dict["explanation"] = explanation
        results.append(row_dict)

    database.clear()
    database.extend(results)

    return {"message": "Pipeline executed", "records": len(results)}


@app.get("/data")
def get_data():
    return database