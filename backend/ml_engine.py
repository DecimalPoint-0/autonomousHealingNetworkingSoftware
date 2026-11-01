import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

class MLEngine:
    def __init__(self, model_path="network_model.joblib"):
        self.model_path = model_path
        self.model = None
        self.features = ['latency', 'throughput', 'packet_loss', 'cpu_usage', 'error_rate']
        
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            self.train_initial_model()

    def train_initial_model(self):
        print("Training initial anomaly detection model...")
        # Generate some synthetic "normal" data for training
        data = []
        for _ in range(1000):
            data.append({
                "latency": np.random.uniform(10, 35),
                "throughput": np.random.uniform(750, 1050),
                "packet_loss": np.random.uniform(0, 0.6),
                "cpu_usage": np.random.uniform(10, 50),
                "error_rate": np.random.uniform(0, 0.15)
            })
        
        df = pd.DataFrame(data)
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.model.fit(df[self.features])
        self.save_model()
        print("Model trained and saved.")

    def predict(self, metrics):
        """
        Returns -1 for anomaly, 1 for normal.
        """
        if not self.model:
            return 1
        
        df = pd.DataFrame([metrics])
        prediction = self.model.predict(df[self.features])
        return int(prediction[0])

    def save_model(self):
        import joblib
        joblib.dump(self.model, self.model_path)

    def load_model(self):
        import joblib
        self.model = joblib.load(self.model_path)

if __name__ == "__main__":
    engine = MLEngine()
    test_metrics = {
        "latency": 500,
        "throughput": 100,
        "packet_loss": 10,
        "cpu_usage": 90,
        "error_rate": 5
    }
    print(f"Prediction for anomaly: {engine.predict(test_metrics)}") # Should be -1
