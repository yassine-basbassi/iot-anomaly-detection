# Architecture du projet

## 1. Vue générale

Ce projet est une solution IoT de surveillance intelligente d'une machine industrielle.

L'architecture suit le flux suivant :

ESP32 + Capteurs
        ↓
Wi-Fi
        ↓
MQTT
        ↓
Python Subscriber
        ↓
SQLite
        ↓
Data Cleaning
        ↓
Machine Learning
        ↓
Anomaly Detection
        ↓
Streamlit Dashboard


## 2. Couche IoT

L'ESP32 simule une machine industrielle et collecte les données des capteurs.

### Capteurs utilisés

- DHT22 : température et humidité
- MPU6050 : vibration et mouvement
- Courant simulé : consommation électrique

L'ESP32 collecte les données toutes les 5 secondes.


## 3. Communication MQTT

Les données sont transmises avec le protocole MQTT.

### Broker

```text
test.mosquitto.org
Port
1883
Topic
iot/industrial/ESP32_MACHINE_01

Les données sont envoyées au format JSON.

Exemple :

{
    "timestamp": 123456,
    "device_id": "ESP32_MACHINE_01",
    "temperature": 24.0,
    "humidity": 40.0,
    "vibration": 0.0,
    "current": 5.5
}
4. Backend Python

Le subscriber Python reçoit les messages MQTT.

Il effectue les opérations suivantes :

Réception du message MQTT
Lecture du JSON
Ajout de la date de réception serveur
Prédiction Machine Learning
Enregistrement dans SQLite
Affichage du résultat
5. Base de données

SQLite est utilisée pour stocker les données des capteurs.

La table principale est :

sensor_data

Elle contient les champs suivants :

id
timestamp
device_id
temperature
humidity
vibration
current
anomaly
anomaly_score
received_at
6. Data Science

Les données sont nettoyées et préparées avec Pandas.

Les principales opérations sont :

suppression des doublons ;
conversion des types ;
traitement des valeurs manquantes ;
détection des valeurs invalides ;
préparation du dataset ;
analyse statistique ;
analyse des corrélations ;
génération de graphiques.
7. Machine Learning

Le projet utilise principalement l'algorithme :

Isolation Forest

Isolation Forest permet d'identifier automatiquement les observations inhabituelles dans les données des capteurs.

Les variables utilisées par le modèle sont :

temperature
humidity
vibration
current

Le modèle produit deux résultats :

anomaly
anomaly_score

Interprétation :

0 = NORMAL
1 = ANOMALY

Un score d'anomalie plus faible indique généralement une observation plus inhabituelle.

8. Détection en temps réel

Lorsqu'un nouveau message MQTT arrive, le système peut effectuer automatiquement une prédiction.

Le flux est :

Nouveau message MQTT
        ↓
Lecture des données
        ↓
Isolation Forest
        ↓
Calcul anomaly_score
        ↓
Classification NORMAL / ANOMALY
        ↓
Enregistrement SQLite
9. Dashboard

Le dashboard est développé avec Streamlit.

Il permet de visualiser :

nombre total de mesures ;
nombre de mesures normales ;
nombre d'anomalies ;
taux d'anomalies ;
température ;
humidité ;
vibration ;
courant ;
score d'anomalie ;
historique complet des données.

Les données du dashboard sont récupérées directement depuis SQLite.

10. Tests

Le projet utilise Pytest pour automatiser les tests.

Les tests vérifient notamment :

la prédiction Machine Learning ;
le fonctionnement de la base SQLite ;
la présence des données ;
la structure des anomalies.

Commande :

pytest -v

Les tests actuels couvrent notamment :

tests/test_ml_predict.py
tests/test_database.py
11. Simulation

Le projet utilise Wokwi pour simuler l'ESP32 et les capteurs.

Cette simulation permet de reproduire le fonctionnement d'une machine IoT sans matériel physique.

Les valeurs normales et anormales peuvent être simulées afin de tester le système de détection.

12. Technologies utilisées
Technologie	Utilisation
ESP32	Acquisition des données IoT
DHT22	Température et humidité
MPU6050	Vibration
MQTT	Communication IoT
Wokwi	Simulation ESP32
Python	Backend et Data Science
SQLite	Base de données
Pandas	Traitement des données
NumPy	Calcul scientifique
Scikit-learn	Machine Learning
Joblib	Sauvegarde du modèle
Matplotlib	Visualisation
Streamlit	Dashboard
Pytest	Tests automatisés
13. Architecture des dossiers
iot-anomaly-detection/
│
├── backend/
│   ├── database.py
│   ├── mqtt_subscriber.py
│   └── config.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── data_science/
│   ├── __init__.py
│   ├── data_cleaning.py
│   ├── exploratory_analysis.py
│   ├── anomaly_detection.py
│   └── ml_predict.py
│
├── dashboard/
│   └── app.py
│
├── firmware/
│   ├── diagram.json
│   ├── esp32_machine.ino
│   └── wokwi.toml
│
├── models/
│   └── isolation_forest.joblib
│
├── reports/
│   └── figures/
│
├── tests/
│   ├── test_database.py
│   └── test_ml_predict.py
│
├── docs/
│   ├── architecture.md
│   └── machine-learning.md
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
14. Résumé du fonctionnement

Le système complet fonctionne selon le schéma suivant :

                    ┌──────────────────┐
                    │      ESP32       │
                    │   DHT22/MPU6050 │
                    └────────┬─────────┘
                             │
                             │ Wi-Fi
                             ▼
                    ┌──────────────────┐
                    │   MQTT Broker    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Python Subscriber│
                    └────────┬─────────┘
                             │
                    ┌────────┴─────────┐
                    ▼                  ▼
              ┌──────────┐      ┌──────────────┐
              │  SQLite  │      │ Machine      │
              │ Database │      │ Learning     │
              └────┬─────┘      └──────┬───────┘
                   │                   │
                   └─────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │    Streamlit     │
                    │    Dashboard     │
                    └──────────────────┘

Cette architecture permet de combiner IoT, communication réseau, stockage de données, Data Science, Machine Learning et visualisation dans une seule application.