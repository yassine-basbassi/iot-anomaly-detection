import json

import paho.mqtt.client as mqtt

from database import init_database, insert_data


# ============================================================
# CONFIGURATION MQTT
# ============================================================

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883

MQTT_TOPIC = "iot/industrial/ESP32_MACHINE_01"


# ============================================================
# CONNEXION MQTT
# ============================================================

def on_connect(client, userdata, flags, reason_code, properties):
    """
    Appelée lorsque Python se connecte au broker MQTT.
    """

    if reason_code == 0:

        print("------------------------------------")
        print("Connected to MQTT broker")
        print("Broker:", MQTT_BROKER)
        print("Topic:", MQTT_TOPIC)
        print("------------------------------------")

        client.subscribe(MQTT_TOPIC)

        print("Waiting for IoT data...")
        print()

    else:

        print("MQTT connection failed")
        print("Reason code:", reason_code)


# ============================================================
# RÉCEPTION DES MESSAGES
# ============================================================

def on_message(client, userdata, message):
    """
    Appelée lorsqu'un message MQTT est reçu.
    """

    try:

        # Message MQTT → texte
        payload = message.payload.decode("utf-8")

        # JSON → dictionnaire Python
        data = json.loads(payload)

        # Récupération des données
        timestamp = data.get("timestamp")
        device_id = data.get("device_id")
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        vibration = data.get("vibration")
        current = data.get("current")

        # Pour le moment, l'anomalie est à 0.
        # Isolation Forest sera intégré plus tard.
        anomaly = 0
        anomaly_score = None

        # ----------------------------------------------------
        # AFFICHAGE
        # ----------------------------------------------------

        print("========== MQTT DATA ==========")

        print("Device      :", device_id)
        print("Timestamp   :", timestamp)
        print("Temperature :", temperature, "°C")
        print("Humidity    :", humidity, "%")
        print("Vibration   :", vibration)
        print("Current     :", current, "A")

        # ----------------------------------------------------
        # SAUVEGARDE SQLITE
        # ----------------------------------------------------

        insert_data(
            timestamp=timestamp,
            device_id=device_id,
            temperature=temperature,
            humidity=humidity,
            vibration=vibration,
            current=current,
            anomaly=anomaly,
            anomaly_score=anomaly_score
        )

        print("Database    : SAVED")
        print("================================")
        print()

    except json.JSONDecodeError:

        print("ERROR: Invalid JSON received")

        print("Raw message:", message.payload)

    except Exception as error:

        print("ERROR:", error)


# ============================================================
# INITIALISATION DATABASE
# ============================================================

init_database()


# ============================================================
# CRÉATION DU CLIENT MQTT
# ============================================================

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="PYTHON_SUBSCRIBER_01"
)


# ============================================================
# CALLBACKS
# ============================================================

client.on_connect = on_connect
client.on_message = on_message


# ============================================================
# CONNEXION
# ============================================================

print("------------------------------------")
print("Python MQTT Subscriber")
print("------------------------------------")

print("Connecting to MQTT broker...")

client.connect(
    MQTT_BROKER,
    MQTT_PORT,
    60
)


# ============================================================
# BOUCLE MQTT
# ============================================================

try:

    print("Starting MQTT loop...")

    client.loop_forever()

except KeyboardInterrupt:

    print()
    print("Subscriber stopped by user.")

finally:

    client.disconnect()

    print("Disconnected from MQTT broker.")