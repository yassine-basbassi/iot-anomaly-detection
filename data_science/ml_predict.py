# ============================================================
# ML PREDICTION MODULE
# IoT Industrial Machine Monitoring
# ============================================================

from pathlib import Path

import joblib
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "isolation_forest.joblib"
)


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


# ============================================================
# PREDICT ANOMALY
# ============================================================

def predict_anomaly(
    temperature,
    humidity,
    vibration,
    current
):

    model = load_model()

    data = pd.DataFrame(
        [
            {
                "temperature": temperature,
                "humidity": humidity,
                "vibration": vibration,
                "current": current
            }
        ]
    )

    prediction = model.predict(data)[0]

    score = model.decision_function(data)[0]

    anomaly = 1 if prediction == -1 else 0

    return anomaly, float(score)