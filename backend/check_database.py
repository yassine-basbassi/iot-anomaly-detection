from database import get_data, get_latest_data, get_anomalies


def main():
    print("------------------------------------")
    print("DATABASE VALIDATION")
    print("------------------------------------")

    # Toutes les mesures
    rows = get_data()

    print("Total measurements:", len(rows))

    # Dernière mesure
    latest = get_latest_data()

    print()
    print("Latest measurement:")

    if latest:
        print("ID          :", latest[0])
        print("Timestamp   :", latest[1])
        print("Device      :", latest[2])
        print("Temperature :", latest[3])
        print("Humidity    :", latest[4])
        print("Vibration   :", latest[5])
        print("Current     :", latest[6])
        print("Anomaly     :", latest[7])
        print("Score       :", latest[8])
    else:
        print("No data found.")

    # Anomalies
    anomalies = get_anomalies()

    print()
    print("Anomalies:", len(anomalies))

    print("------------------------------------")


if __name__ == "__main__":
    main()