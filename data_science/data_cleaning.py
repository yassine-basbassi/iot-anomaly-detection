import sys
from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURATION DU PROJET
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR))


from backend.database import get_data


# ============================================================
# DOSSIERS
# ============================================================

RAW_DIR = BASE_DIR / "data" / "raw"

PROCESSED_DIR = BASE_DIR / "data" / "processed"


RAW_FILE = RAW_DIR / "sensor_data_raw.csv"

PROCESSED_FILE = PROCESSED_DIR / "sensor_data_clean.csv"


# ============================================================
# COLONNES
# ============================================================

COLUMNS = [
    "id",
    "timestamp",
    "device_id",
    "temperature",
    "humidity",
    "vibration",
    "current",
    "anomaly",
    "anomaly_score",
    "received_at"
]


NUMERIC_COLUMNS = [
    "temperature",
    "humidity",
    "vibration",
    "current",
    "anomaly",
    "anomaly_score"
]


# ============================================================
# CHARGER LES DONNÉES
# ============================================================

def load_data():

    rows = get_data()

    df = pd.DataFrame(
        rows,
        columns=COLUMNS
    )

    return df


# ============================================================
# NETTOYAGE
# ============================================================

def clean_data(df):

    df = df.copy()

    print()
    print("========== CLEANING DATA ==========")

    print("Initial rows:", len(df))

    # --------------------------------------------------------
    # Nettoyage texte
    # --------------------------------------------------------

    df["timestamp"] = (
        df["timestamp"]
        .astype(str)
        .str.strip()
    )

    df["device_id"] = (
        df["device_id"]
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # Conversion des données numériques
    # --------------------------------------------------------

    for column in NUMERIC_COLUMNS:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # --------------------------------------------------------
    # Conversion du timestamp réel
    # --------------------------------------------------------

    df["received_at"] = pd.to_datetime(
        df["received_at"],
        errors="coerce",
        utc=True
    )

    # --------------------------------------------------------
    # Suppression des doublons
    # --------------------------------------------------------

    before_duplicates = len(df)

    df = df.drop_duplicates(
        subset=[
            "timestamp",
            "device_id",
            "temperature",
            "humidity",
            "vibration",
            "current"
        ]
    )

    duplicates_removed = (
        before_duplicates - len(df)
    )

    print(
        "Duplicates removed:",
        duplicates_removed
    )

    # --------------------------------------------------------
    # Vérification des valeurs impossibles
    # --------------------------------------------------------

    invalid_mask = (
        (df["temperature"] < -40) |
        (df["temperature"] > 100) |
        (df["humidity"] < 0) |
        (df["humidity"] > 100) |
        (df["vibration"] < 0) |
        (df["current"] < 0)
    )

    invalid_count = invalid_mask.sum()

    print(
        "Invalid rows:",
        invalid_count
    )

    df = df[~invalid_mask]

    # --------------------------------------------------------
    # Valeurs manquantes
    # --------------------------------------------------------

    required_columns = [
        "timestamp",
        "device_id",
        "temperature",
        "humidity",
        "vibration",
        "current"
    ]

    missing_before = (
        df[required_columns]
        .isnull()
        .sum()
    )

    print()
    print("Missing values before cleaning:")

    print(missing_before)

    df = df.dropna(
        subset=required_columns
    )

    # --------------------------------------------------------
    # Nettoyage de anomaly
    # --------------------------------------------------------

    df["anomaly"] = (
        df["anomaly"]
        .fillna(0)
        .astype(int)
    )

    # --------------------------------------------------------
    # Trier par date de réception
    # --------------------------------------------------------

    df = df.sort_values(
        by="received_at",
        na_position="last"
    )

    # --------------------------------------------------------
    # Résultat
    # --------------------------------------------------------

    print()
    print("Final rows:", len(df))

    print()
    print("Data types:")

    print(df.dtypes)

    print()
    print("========== CLEANING COMPLETE ==========")

    return df


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():

    RAW_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Charger depuis SQLite
    # --------------------------------------------------------

    df = load_data()

    if df.empty:

        print("No data found in database.")

        return

    # --------------------------------------------------------
    # Sauvegarder les données brutes
    # --------------------------------------------------------

    df.to_csv(
        RAW_FILE,
        index=False
    )

    print()
    print("Raw data saved to:")

    print(RAW_FILE)

    # --------------------------------------------------------
    # Nettoyer
    # --------------------------------------------------------

    df_clean = clean_data(df)

    # --------------------------------------------------------
    # Sauvegarder les données nettoyées
    # --------------------------------------------------------

    df_clean.to_csv(
        PROCESSED_FILE,
        index=False
    )

    print()
    print("Clean data saved to:")

    print(PROCESSED_FILE)

    # --------------------------------------------------------
    # Aperçu
    # --------------------------------------------------------

    print()
    print("========== DATA PREVIEW ==========")

    print(
        df_clean.head()
    )

    print()
    print("Dataset shape:")

    print(
        df_clean.shape
    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()