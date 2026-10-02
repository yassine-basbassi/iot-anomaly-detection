import sqlite3
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATABASE_PATH = DATA_DIR / "sensor_data.db"


# ============================================================
# INITIALISATION DE LA BASE
# ============================================================

def init_database():
    """
    Crée le dossier data et la table sensor_data
    si elle n'existe pas.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            device_id TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            vibration REAL,
            current REAL,
            anomaly INTEGER DEFAULT 0,
            anomaly_score REAL
        )
        """
    )

    connection.commit()
    connection.close()


# ============================================================
# INSERTION DES DONNÉES
# ============================================================

def insert_data(
    timestamp,
    device_id,
    temperature,
    humidity,
    vibration,
    current,
    anomaly=0,
    anomaly_score=None
):
    """
    Insère une mesure IoT dans la base SQLite.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO sensor_data (
            timestamp,
            device_id,
            temperature,
            humidity,
            vibration,
            current,
            anomaly,
            anomaly_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            timestamp,
            device_id,
            temperature,
            humidity,
            vibration,
            current,
            anomaly,
            anomaly_score
        )
    )

    connection.commit()
    connection.close()


# ============================================================
# RÉCUPÉRER TOUTES LES DONNÉES
# ============================================================

def get_data():
    """
    Retourne toutes les mesures enregistrées.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            timestamp,
            device_id,
            temperature,
            humidity,
            vibration,
            current,
            anomaly,
            anomaly_score
        FROM sensor_data
        ORDER BY id ASC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# RÉCUPÉRER LA DERNIÈRE MESURE
# ============================================================

def get_latest_data():
    """
    Retourne la dernière mesure enregistrée.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            timestamp,
            device_id,
            temperature,
            humidity,
            vibration,
            current,
            anomaly,
            anomaly_score
        FROM sensor_data
        ORDER BY id DESC
        LIMIT 1
        """
    )

    row = cursor.fetchone()

    connection.close()

    return row


# ============================================================
# RÉCUPÉRER LES ANOMALIES
# ============================================================

def get_anomalies():
    """
    Retourne uniquement les mesures considérées
    comme des anomalies.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            timestamp,
            device_id,
            temperature,
            humidity,
            vibration,
            current,
            anomaly,
            anomaly_score
        FROM sensor_data
        WHERE anomaly = 1
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows