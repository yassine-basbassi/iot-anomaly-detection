# ============================================================
# ANOMALY DETECTION
# IoT Industrial Machine Monitoring
# ============================================================

from pathlib import Path
import sys

import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "sensor_data_clean.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "isolation_forest.joblib"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "sensor_data_analyzed.csv"
)


# ============================================================
# IMPORT DATABASE
# ============================================================

sys.path.insert(0, str(BASE_DIR))

from backend.database import update_anomaly_results


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

print("\n========== LOADING DATA ==========")

df = pd.read_csv(DATA_PATH)

print(f"Dataset shape: {df.shape}")


# ============================================================
# VARIABLES UTILISÉES PAR LE MODÈLE
# ============================================================

FEATURES = [
    "temperature",
    "humidity",
    "vibration",
    "current"
]

X = df[FEATURES].copy()


# ============================================================
# VÉRIFICATION DES DONNÉES
# ============================================================

print("\n========== FEATURES ==========")

print(FEATURES)

print("\nMissing values:")

print(X.isnull().sum())


# ============================================================
# VÉRIFICATION DES DONNÉES MANQUANTES
# ============================================================

if X.isnull().any().any():

    print("\nERROR: Missing values detected.")

    print("Isolation Forest cannot continue.")

    sys.exit(1)


# ============================================================
# MODÈLE ISOLATION FOREST
# ============================================================

print("\n========== ISOLATION FOREST ==========")

model = IsolationForest(
    n_estimators=100,
    contamination="auto",
    random_state=42
)


# ============================================================
# ENTRAÎNEMENT
# ============================================================

print("\n========== MODEL TRAINING ==========")

model.fit(X)

print("Model trained successfully.")


# ============================================================
# SAUVEGARDE DU MODÈLE
# ============================================================

print("\n========== SAVE MODEL ==========")

MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_PATH
)

print("Model saved to:")

print(MODEL_PATH)


# ============================================================
# PRÉDICTION
# ============================================================

print("\n========== PREDICTION ==========")

predictions = model.predict(X)

# Isolation Forest:
#
#  1  = normal
# -1  = anomaly

df["anomaly"] = (
    predictions == -1
).astype(int)

print("Predictions completed.")


# ============================================================
# SCORE D'ANOMALIE
# ============================================================

df["anomaly_score"] = (
    model.decision_function(X)
)

print("Anomaly scores calculated.")


# ============================================================
# RÉSULTATS
# ============================================================

print("\n========== ANOMALY RESULTS ==========")

print(
    df[
        [
            "id",
            "temperature",
            "humidity",
            "vibration",
            "current",
            "anomaly",
            "anomaly_score"
        ]
    ].to_string(index=False)
)


# ============================================================
# STATISTIQUES
# ============================================================

total = len(df)

anomalies = int(
    df["anomaly"].sum()
)

normal = total - anomalies


print("\n========== SUMMARY ==========")

print(f"Total samples : {total}")

print(f"Normal        : {normal}")

print(f"Anomalies     : {anomalies}")


if total > 0:

    anomaly_rate = (
        anomalies / total * 100
    )

    print(
        f"Anomaly rate  : {anomaly_rate:.2f}%"
    )


# ============================================================
# MISE À JOUR DE SQLITE
# ============================================================

print("\n========== UPDATE SQLITE ==========")

results = (
    df[
        [
            "id",
            "anomaly",
            "anomaly_score"
        ]
    ]
    .to_dict("records")
)

update_anomaly_results(results)

print(
    "SQLite database updated successfully."
)


# ============================================================
# SAUVEGARDE DU DATASET ANALYSÉ
# ============================================================

print("\n========== SAVE ANALYZED DATA ==========")

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("Analyzed dataset saved to:")

print(OUTPUT_PATH)


# ============================================================
# FIN
# ============================================================

print(
    "\n========== ANOMALY DETECTION COMPLETE =========="
)