class ExplanationAgent:
    def explain(self, row):
        if row["amount"] > 3000:
            return "🚨 High transaction amount detected"
        elif row["time"] < 5:
            return "⚠️ Unusual transaction time"
        else:
            return "⚠️ Pattern deviation detected"
class ExplanationAgent:
    def explain(self, row):
        if row["amount"] > 4000:
            return "🚨 Critical anomaly: Extremely high transaction, possible fraud spike."
        elif row["time"] < 5:
            return "⚠️ Suspicious timing: Activity during unusual hours."
        else:
            return "⚠️ Behavioral anomaly: Pattern deviates from normal trends."