# IoT Anomaly Detection

## Industrial Machine Monitoring with ESP32, MQTT and Machine Learning

Projet de surveillance intelligente d'une machine industrielle combinant **IoT, Data Science et Machine Learning**.

Le système collecte des données depuis un ESP32 simulé avec Wokwi, transmet les mesures via MQTT, les stocke dans une base SQLite et utilise un modèle **Isolation Forest** pour détecter automatiquement les anomalies.

---

## 1. Présentation

L'objectif du projet est de construire un pipeline IoT complet capable de :

- collecter des données de capteurs ;
- transmettre les données avec MQTT ;
- recevoir les données avec Python ;
- stocker les données dans SQLite ;
- nettoyer et préparer les données ;
- analyser les données avec Pandas ;
- détecter automatiquement les anomalies avec Machine Learning ;
- afficher les résultats dans un dashboard Streamlit ;
- tester automatiquement les composants avec Pytest.

---

## 2. Architecture

```text
                    ┌─────────────────────┐
                    │       ESP32         │
                    │                     │
                    │ DHT22 + MPU6050     │
                    │ + Current Sensor    │
                    └──────────┬──────────┘
                               │
                               │ Wi-Fi
                               ▼
                    ┌─────────────────────┐
                    │    MQTT Broker      │
                    │  test.mosquitto.org │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Python Subscriber  │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             ┌─────────────┐      ┌───────────────┐
             │   SQLite    │      │ Machine       │
             │  Database   │      │ Learning      │
             └──────┬──────┘      │ Isolation     │
                    │             │ Forest        │
                    │             └───────┬───────┘
                    │                     │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Streamlit Dashboard │
                    └─────────────────────┘
3. Technologies
Technologie	Utilisation
ESP32	Acquisition IoT
DHT22	Température et humidité
MPU6050	Vibration
MQTT	Communication IoT
Wokwi	Simulation ESP32
Python	Backend et Data Science
SQLite	Stockage des données
Pandas	Data Processing
NumPy	Calcul scientifique
Scikit-learn	Machine Learning
Joblib	Sauvegarde du modèle
Matplotlib	Visualisation
Streamlit	Dashboard
Pytest	Tests automatisés
4. Capteurs
DHT22

Mesure :

température ;
humidité.
MPU6050

Utilisé pour simuler les vibrations et mouvements de la machine.

Courant

Le courant électrique est simulé dans Wokwi afin de représenter la consommation électrique de la machine.

5. Communication MQTT

Le système utilise MQTT pour transmettre les données entre l'ESP32 et le backend Python.

Broker
test.mosquitto.org
Port
1883
Topic
iot/industrial/ESP32_MACHINE_01
Exemple de message
{
    "timestamp": 123456,
    "device_id": "ESP32_MACHINE_01",
    "temperature": 24.0,
    "humidity": 40.0,
    "vibration": 0.0,
    "current": 5.5
}
6. Pipeline Data Science

Les données suivent le pipeline suivant :

IoT Data
   ↓
MQTT
   ↓
SQLite
   ↓
Data Cleaning
   ↓
Exploratory Data Analysis
   ↓
Feature Preparation
   ↓
Isolation Forest
   ↓
Anomaly Detection
   ↓
Streamlit Dashboard
7. Machine Learning

Le projet utilise Isolation Forest, un algorithme de détection d'anomalies non supervisé disponible dans Scikit-learn.

Les variables utilisées sont :

temperature
humidity
vibration
current

Le modèle produit :

anomaly
anomaly_score

Interprétation :

0 → NORMAL
1 → ANOMALY

Le modèle est sauvegardé avec Joblib :

models/isolation_forest.joblib
8. Exemple de détection

Une mesure normale peut être :

Temperature : 24.0 °C
Humidity    : 40.0 %
Vibration   : 0.0
Current     : 2.1 A
Status      : NORMAL

Une mesure anormale simulée :

Temperature : 24.0 °C
Humidity    : 40.0 %
Vibration   : 0.0
Current     : 5.5 A
Status      : ANOMALY
9. Résultats

Lors d'un test avec les données simulées :

Total observations : 20
Normal             : 14
Anomalies           : 6
Taux d'anomalies    : 30 %

Les anomalies détectées correspondaient principalement aux observations présentant un courant de 5.5 A.

10. Dashboard

Le dashboard Streamlit permet de visualiser :

nombre total de mesures ;
mesures normales ;
anomalies ;
taux d'anomalies ;
température ;
humidité ;
vibration ;
courant ;
anomaly score ;
historique des données.

Pour lancer le dashboard :

streamlit run dashboard/app.py
11. Tests

Le projet utilise Pytest.

Les tests couvrent actuellement :

tests/test_ml_predict.py
tests/test_database.py

Pour lancer tous les tests :

pytest -v

Résultat attendu :

6 passed
12. Installation
Cloner le projet
git clone https://github.com/yassine-basbassi/iot-anomaly-detection.git

Entrer dans le projet :

cd iot-anomaly-detection
Installer les dépendances
python -m pip install -r requirements.txt
13. Exécution
Étape 1 — ESP32

Ouvrir le projet dans Wokwi et démarrer la simulation.

Étape 2 — Subscriber MQTT

Dans un terminal :

python backend/mqtt_subscriber.py
Étape 3 — Dashboard

Dans un autre terminal :

streamlit run dashboard/app.py
Étape 4 — Tests
pytest -v
14. Structure du projet
iot-anomaly-detection/
│
├── backend/
│   ├── config.py
│   ├── database.py
│   └── mqtt_subscriber.py
│
├── dashboard/
│   └── app.py
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
├── docs/
│   ├── architecture.md
│   └── machine-learning.md
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
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
15. Limites du projet

Le projet est actuellement basé sur une simulation Wokwi.

Les principales limites sont :

données simulées ;
nombre limité d'observations ;
anomalies générées artificiellement ;
absence de capteurs industriels physiques ;
modèle entraîné sur un petit dataset.

Les résultats représentent donc une démonstration technique du pipeline IoT + Data Science + Machine Learning.

16. Améliorations futures

Les évolutions possibles sont :

capteurs physiques réels ;
PostgreSQL ;
FastAPI ;
Docker ;
Grafana ;
Cloud IoT ;
MQTT sécurisé avec TLS ;
système d'alertes ;
maintenance prédictive ;
XGBoost ;
Local Outlier Factor ;
One-Class SVM ;
LSTM pour les séries temporelles.
17. Objectif professionnel

Ce projet a été réalisé dans le cadre d'un parcours orienté :

Data Science + IoT + Machine Learning + AIoT

Il constitue un projet de portfolio permettant de démontrer des compétences en :

développement Python ;
IoT ;
MQTT ;
traitement des données ;
Machine Learning ;
détection d'anomalies ;
bases de données ;
visualisation ;
tests automatisés ;
développement d'applications Data.
18. Auteur

Yassine Basbassi

Projet personnel — IoT / Data Science / Machine Learning.