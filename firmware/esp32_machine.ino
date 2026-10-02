import time
import math
import network
import ujson
import dht

from machine import Pin, I2C
from umqtt.simple import MQTTClient


# ============================================================
# CONFIGURATION WIFI
# ============================================================

WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""


# ============================================================
# CONFIGURATION MQTT
# ============================================================

MQTT_CLIENT_ID = "ESP32_MACHINE_01"
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/industrial/ESP32_MACHINE_01"


# ============================================================
# CAPTEURS
# ============================================================

DHT_PIN = 4

LED_GREEN_PIN = 27
LED_RED_PIN = 26

I2C_SDA = 21
I2C_SCL = 22

MPU6050_ADDRESS = 0x68


# ============================================================
# SEUILS D'ANOMALIE
# ============================================================

TEMPERATURE_LIMIT = 35.0
VIBRATION_LIMIT = 1.50
CURRENT_LIMIT = 4.50


# ============================================================
# INITIALISATION
# ============================================================

dht_sensor = dht.DHT22(Pin(DHT_PIN))

green_led = Pin(LED_GREEN_PIN, Pin.OUT)
red_led = Pin(LED_RED_PIN, Pin.OUT)

i2c = I2C(
    0,
    scl=Pin(I2C_SCL),
    sda=Pin(I2C_SDA),
    freq=400000
)


# ============================================================
# WIFI
# ============================================================

def connect_wifi():

    print("Connecting to WiFi", end="")

    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    if not wifi.isconnected():
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)

        while not wifi.isconnected():
            print(".", end="")
            time.sleep(0.2)

    print(" Connected!")

    print("IP address:", wifi.ifconfig()[0])


# ============================================================
# MQTT
# ============================================================

def connect_mqtt():

    print("Connecting to MQTT server...", end=" ")

    client = MQTTClient(
        MQTT_CLIENT_ID,
        MQTT_BROKER,
        port=MQTT_PORT
    )

    client.connect()

    print("Connected!")

    return client


# ============================================================
# MPU6050
# ============================================================

def init_mpu6050():

    devices = i2c.scan()

    print("I2C devices:", devices)

    if MPU6050_ADDRESS not in devices:
        raise Exception("MPU6050 not detected")

    # Wake up MPU6050
    i2c.writeto_mem(
        MPU6050_ADDRESS,
        0x6B,
        b"\x00"
    )

    print("MPU6050 detected!")


def read_mpu6050():

    data = i2c.readfrom_mem(
        MPU6050_ADDRESS,
        0x3B,
        6
    )

    ax_raw = (data[0] << 8) | data[1]
    ay_raw = (data[2] << 8) | data[3]
    az_raw = (data[4] << 8) | data[5]

    if ax_raw >= 32768:
        ax_raw -= 65536

    if ay_raw >= 32768:
        ay_raw -= 65536

    if az_raw >= 32768:
        az_raw -= 65536

    ax = ax_raw / 16384.0
    ay = ay_raw / 16384.0
    az = az_raw / 16384.0

    magnitude = math.sqrt(
        ax * ax +
        ay * ay +
        az * az
    )

    vibration = abs(magnitude - 1.0)

    return vibration


# ============================================================
# CURRENT SIMULATION
# ============================================================

def simulate_current():

    seconds = time.ticks_ms() // 1000

    # Anomaly between 20s and 30s
    if (seconds % 30) >= 20:
        return 5.5

    return 2.1


# ============================================================
# ANOMALY DETECTION
# ============================================================

def detect_anomaly(temperature, vibration, current):

    if temperature > TEMPERATURE_LIMIT:
        return True

    if vibration > VIBRATION_LIMIT:
        return True

    if current > CURRENT_LIMIT:
        return True

    return False


# ============================================================
# LED STATUS
# ============================================================

def update_leds(anomaly):

    if anomaly:

        green_led.off()
        red_led.on()

    else:

        green_led.on()
        red_led.off()


# ============================================================
# MAIN PROGRAM
# ============================================================

print("------------------------------------")
print("IoT Industrial Machine Monitoring")
print("ESP32 + DHT22 + MPU6050 + MQTT")
print("------------------------------------")


# WiFi
connect_wifi()


# MPU6050
print("Scanning I2C...")
init_mpu6050()


# MQTT
mqtt_client = connect_mqtt()


print("------------------------------------")
print("System ready!")
print("MQTT Topic:", MQTT_TOPIC)
print("------------------------------------")


while True:

    try:

        # ----------------------------------------------------
        # Lecture DHT22
        # ----------------------------------------------------

        dht_sensor.measure()

        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()


        # ----------------------------------------------------
        # Lecture vibration
        # ----------------------------------------------------

        vibration = read_mpu6050()


        # ----------------------------------------------------
        # Simulation courant
        # ----------------------------------------------------

        current = simulate_current()


        # ----------------------------------------------------
        # Détection anomalie
        # ----------------------------------------------------

        anomaly = detect_anomaly(
            temperature,
            vibration,
            current
        )


        # ----------------------------------------------------
        # LED
        # ----------------------------------------------------

        update_leds(anomaly)


        # ----------------------------------------------------
        # Création du message JSON
        # ----------------------------------------------------

        payload = {
            "timestamp": time.ticks_ms(),
            "device_id": MQTT_CLIENT_ID,
            "temperature": temperature,
            "humidity": humidity,
            "vibration": vibration,
            "current": current
        }


        message = ujson.dumps(payload)


        # ----------------------------------------------------
        # Publication MQTT
        # ----------------------------------------------------

        mqtt_client.publish(
            MQTT_TOPIC,
            message
        )


        # ----------------------------------------------------
        # Affichage
        # ----------------------------------------------------

        print()
        print("========== MACHINE DATA ==========")

        print("Temperature :", temperature, "C")
        print("Humidity    :", humidity, "%")
        print("Vibration   :", vibration)
        print("Current     :", current, "A")

        if anomaly:
            print("Status      : ANOMALY")
        else:
            print("Status      : NORMAL")

        print("MQTT        : PUBLISHED")
        print("Topic       :", MQTT_TOPIC)
        print("Payload     :", message)

        print("==================================")


        time.sleep(5)


    except Exception as e:

        print("ERROR:", e)

        green_led.off()
        red_led.on()

        time.sleep(5)