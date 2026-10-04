import sys
from pathlib import Path

# Ajouter la racine du projet au chemin Python
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from data_science.ml_predict import predict_anomaly


def test_predict_normal_data():
    anomaly, score = predict_anomaly(
        temperature=24.0,
        humidity=40.0,
        vibration=0.0,
        current=2.1
    )

    assert anomaly in [0, 1]
    assert isinstance(score, float)


def test_predict_anomaly_data():
    anomaly, score = predict_anomaly(
        temperature=24.0,
        humidity=40.0,
        vibration=0.0,
        current=5.5
    )

    assert anomaly == 1
    assert isinstance(score, float)


def test_score_is_numeric():
    anomaly, score = predict_anomaly(
        temperature=30.0,
        humidity=50.0,
        vibration=0.5,
        current=3.0
    )

    assert isinstance(anomaly, int)
    assert isinstance(score, float)