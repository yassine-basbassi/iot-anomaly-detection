# ============================================================
# EXPLORATORY DATA ANALYSIS
# IoT Industrial Machine Monitoring
# ============================================================

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "sensor_data_clean.csv"

FIGURES_DIR = BASE_DIR / "reports" / "figures"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

print("\n========== LOADING DATA ==========")

df = pd.read_csv(DATA_PATH)

print(f"Dataset loaded from:")
print(DATA_PATH)

print(f"\nDataset shape: {df.shape}")


# ============================================================
# INFORMATIONS GÉNÉRALES
# ============================================================

print("\n========== DATA INFORMATION ==========")

print(df.info())


# ============================================================
# STATISTIQUES DESCRIPTIVES
# ============================================================

print("\n========== DESCRIPTIVE STATISTICS ==========")

print(df.describe())


# ============================================================
# VALEURS MANQUANTES
# ============================================================

print("\n========== MISSING VALUES ==========")

print(df.isnull().sum())


# ============================================================
# VARIABLES SENSORIELLES
# ============================================================

sensor_columns = [
    "temperature",
    "humidity",
    "vibration",
    "current"
]

print("\n========== SENSOR STATISTICS ==========")

for column in sensor_columns:

    print(f"\n--- {column.upper()} ---")

    print(f"Mean : {df[column].mean():.2f}")
    print(f"Min  : {df[column].min():.2f}")
    print(f"Max  : {df[column].max():.2f}")
    print(f"Std  : {df[column].std():.2f}")


# ============================================================
# CORRÉLATION
# ============================================================

print("\n========== CORRELATION MATRIX ==========")

correlation = df[sensor_columns].corr()

print(correlation)


# ============================================================
# GRAPHIQUE 1 : TEMPÉRATURE
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    df["temperature"],
    marker="o"
)

plt.title("Temperature Evolution")
plt.xlabel("Sample")
plt.ylabel("Temperature (°C)")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "temperature.png"
)

plt.show()


# ============================================================
# GRAPHIQUE 2 : HUMIDITÉ
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    df["humidity"],
    marker="o"
)

plt.title("Humidity Evolution")
plt.xlabel("Sample")
plt.ylabel("Humidity (%)")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "humidity.png"
)

plt.show()


# ============================================================
# GRAPHIQUE 3 : VIBRATION
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    df["vibration"],
    marker="o"
)

plt.title("Vibration Evolution")
plt.xlabel("Sample")
plt.ylabel("Vibration")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "vibration.png"
)

plt.show()


# ============================================================
# GRAPHIQUE 4 : COURANT
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    df["current"],
    marker="o"
)

plt.title("Current Evolution")
plt.xlabel("Sample")
plt.ylabel("Current (A)")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "current.png"
)

plt.show()


# ============================================================
# GRAPHIQUE 5 : MATRICE DE CORRÉLATION
# ============================================================

plt.figure(figsize=(8, 6))

plt.imshow(
    correlation,
    interpolation="nearest"
)

plt.title("Sensor Correlation Matrix")

plt.xticks(
    range(len(sensor_columns)),
    sensor_columns,
    rotation=45
)

plt.yticks(
    range(len(sensor_columns)),
    sensor_columns
)

plt.colorbar()

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "correlation_matrix.png"
)

plt.show()


# ============================================================
# RÉSUMÉ
# ============================================================

print("\n========== EDA COMPLETE ==========")

print(f"Figures saved in:")
print(FIGURES_DIR)