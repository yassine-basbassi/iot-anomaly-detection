import sys
from pathlib import Path

# Ajouter la racine du projet au chemin Python
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.database import get_data, get_latest_data, get_anomalies


def test_database_contains_data():
    data = get_data()

    assert data is not None
    assert len(data) > 0


def test_latest_data_exists():
    latest = get_latest_data()

    assert latest is not None
    assert len(latest) == 10


def test_anomalies_have_correct_structure():
    anomalies = get_anomalies()

    for anomaly in anomalies:
        assert len(anomaly) == 10
        assert anomaly[7] == 1
        assert anomaly[8] is not None