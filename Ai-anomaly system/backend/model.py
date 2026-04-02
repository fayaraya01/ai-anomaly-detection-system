from sklearn.ensemble import IsolationForest

class DetectionAgent:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05)

    def detect(self, data):
        preds = self.model.fit_predict(data[["amount", "time"]])
        return [1 if p == -1 else 0 for p in preds]