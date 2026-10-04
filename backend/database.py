import sqlite3
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATABASE_PATH = DATA_DIR / "sensor_data.db"


# ============================================================
# INITIALISATION / MIGRATION
# ============================================================

def init_database():
    """
    Crée la base si nécessaire et ajoute les nouvelles colonnes
    si elles n'existent pas encore.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    # --------------------------------------------------------
    # Création de la table
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            device_id TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            vibration REAL,
            current REAL,
            anomaly INTEGER DEFAULT 0,
            anomaly_score REAL,
            received_at TEXT
        )
    """)

    # --------------------------------------------------------
    # Vérifier les colonnes existantes
    # --------------------------------------------------------

    cursor.execute("""
        PRAGMA table_info(sensor_data)
    """)

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    # --------------------------------------------------------
    # Ajouter received_at si nécessaire
    # --------------------------------------------------------

    if "received_at" not in columns:

        cursor.execute("""
            ALTER TABLE sensor_data
            ADD COLUMN received_at TEXT
        """)

        print("Database migration: received_at added.")

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
    anomaly_score=None,
    received_at=None
):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO sensor_data (
            timestamp,
            device_id,
            temperature,
            humidity,
            vibration,
            current,
            anomaly,
            anomaly_score,
            received_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        device_id,
        temperature,
        humidity,
        vibration,
        current,
        anomaly,
        anomaly_score,
        received_at
    ))

    connection.commit()

    connection.close()


# ============================================================
# RÉCUPÉRER TOUTES LES DONNÉES
# ============================================================

def get_data():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            timestamp,
            device_id,
            temperature,
            humidity,
            vibration,
            current,
            anomaly,
            anomaly_score,
            received_at
        FROM sensor_data
        ORDER BY id
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# DERNIÈRE MESURE
# ============================================================

def get_latest_data():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            timestamp,
            device_id,
            temperature,
            humidity,
            vibration,
            current,
            anomaly,
            anomaly_score,
            received_at
        FROM sensor_data
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    connection.close()

    return row


# ============================================================
# RÉCUPÉRER LES ANOMALIES
# ============================================================

def get_anomalies():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            timestamp,
            device_id,
            temperature,
            humidity,
            vibration,
            current,
            anomaly,
            anomaly_score,
            received_at
        FROM sensor_data
        WHERE anomaly = 1
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    init_database()

    print("------------------------------------")
    print("DATABASE INITIALIZED")
    print("------------------------------------")
    print("Database:", DATABASE_PATH)

# ============================================================
# UPDATE MACHINE LEARNING RESULTS
# ============================================================

def update_anomaly_results(results):
    """
    Met à jour les colonnes anomaly et anomaly_score
    dans la base SQLite.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    for result in results:

        cursor.execute(
            """
            UPDATE sensor_data
            SET anomaly = ?,
                anomaly_score = ?
            WHERE id = ?
            """,
            (
                int(result["anomaly"]),
                float(result["anomaly_score"]),
                int(result["id"])
            )
        )

    connection.commit()

    connection.close()