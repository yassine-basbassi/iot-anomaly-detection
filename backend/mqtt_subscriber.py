# ============================================================
# MQTT SUBSCRIBER
# IoT Industrial Machine Monitoring
# ============================================================

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import paho.mqtt.client as mqtt


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR))


# ============================================================
# DATABASE
# ============================================================

from backend.database import insert_data


# ============================================================
# MACHINE LEARNING
# ============================================================

from data_science.ml_predict import predict_anomaly


# ============================================================
# MQTT CONFIGURATION
# ============================================================

MQTT_BROKER = "test.mosquitto.org"

MQTT_PORT = 1883

MQTT_TOPIC = "iot/industrial/ESP32_MACHINE_01"

CLIENT_ID = "PYTHON_SUBSCRIBER_01"


# ============================================================
# CALLBACK : CONNECT
# ============================================================

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("\n========================================")
        print("MQTT CONNECTED")
        print("Broker :", MQTT_BROKER)
        print("Topic  :", MQTT_TOPIC)
        print("========================================\n")

        client.subscribe(MQTT_TOPIC)

        print("Waiting for ESP32 data...\n")

    else:

        print(
            f"MQTT connection failed. Return code: {rc}"
        )


# ============================================================
# CALLBACK : MESSAGE
# ============================================================

def on_message(client, userdata, msg):

    try:

        # ----------------------------------------------------
        # JSON MESSAGE
        # ----------------------------------------------------

        payload = msg.payload.decode("utf-8")

        data = json.loads(payload)


        # ----------------------------------------------------
        # SENSOR DATA
        # ----------------------------------------------------

        timestamp = data["timestamp"]

        device_id = data["device_id"]

        temperature = float(
            data["temperature"]
        )

        humidity = float(
            data["humidity"]
        )

        vibration = float(
            data["vibration"]
        )

        current = float(
            data["current"]
        )


        # ----------------------------------------------------
        # SERVER TIMESTAMP
        # ----------------------------------------------------

        received_at = datetime.now(
            timezone.utc
        ).isoformat(
            timespec="seconds"
        )


        # ----------------------------------------------------
        # MACHINE LEARNING
        # ----------------------------------------------------

        anomaly, anomaly_score = predict_anomaly(
            temperature,
            humidity,
            vibration,
            current
        )


        # ----------------------------------------------------
        # SAVE TO DATABASE
        # ----------------------------------------------------

        insert_data(
            timestamp=timestamp,
            device_id=device_id,
            temperature=temperature,
            humidity=humidity,
            vibration=vibration,
            current=current,
            anomaly=anomaly,
            anomaly_score=anomaly_score,
            received_at=received_at
        )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        if anomaly == 1:

            status = "ANOMALY"

        else:

            status = "NORMAL"


        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------

        print("\n========== MQTT DATA ==========")

        print(
            f"Device      : {device_id}"
        )

        print(
            f"ESP32 Time  : {timestamp}"
        )

        print(
            f"Received At : {received_at}"
        )

        print(
            f"Temperature : {temperature} °C"
        )

        print(
            f"Humidity    : {humidity} %"
        )

        print(
            f"Vibration   : {vibration}"
        )

        print(
            f"Current     : {current} A"
        )

        print(
            f"Anomaly     : {anomaly}"
        )

        print(
            f"Score       : {anomaly_score:.6f}"
        )

        print(
            f"Status      : {status}"
        )

        print(
            "Database    : SAVED"
        )

        print(
            "================================"
        )


    except Exception as error:

        print(
            "\nERROR processing MQTT message:"
        )

        print(error)


# ============================================================
# MQTT CLIENT
# ============================================================

client = mqtt.Client(
    client_id=CLIENT_ID
)

client.on_connect = on_connect

client.on_message = on_message


# ============================================================
# CONNECT
# ============================================================

print("\nConnecting to MQTT broker...")

client.connect(
    MQTT_BROKER,
    MQTT_PORT,
    60
)


# ============================================================
# START LOOP
# ============================================================

client.loop_forever()