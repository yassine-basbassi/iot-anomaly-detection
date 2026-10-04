 Machine Learning

## 1. Objectif

L'objectif du Machine Learning dans ce projet est de détecter automatiquement les comportements anormaux d'une machine industrielle à partir des données provenant des capteurs IoT.

Les données utilisées sont :

- température ;
- humidité ;
- vibration ;
- courant électrique.

Le système doit identifier les mesures normales et les mesures inhabituelles.

---

## 2. Algorithme utilisé

Le projet utilise principalement l'algorithme **Isolation Forest** de Scikit-learn.

Isolation Forest est un algorithme de détection d'anomalies non supervisé.

Il est adapté à ce projet car nous ne disposons pas initialement d'un ensemble de données étiqueté indiquant précisément quelles mesures sont normales ou anormales.

---

## 3. Variables utilisées

Le modèle utilise quatre variables :

```text
temperature
humidity
vibration
current

Exemple d'une observation :

Temperature : 24.0 °C
Humidity    : 40.0 %
Vibration   : 0.0
Current     : 2.1 A

Cette observation correspond à un fonctionnement normal.

4. Détection d'une anomalie

Le modèle retourne une prédiction :

1  → anomalie
0  → fonctionnement normal

Le modèle fournit également un anomaly_score.

Le score permet de mesurer à quel point une observation est inhabituelle.

Un score plus faible correspond généralement à une observation plus anormale.

5. Exemple dans le projet

Dans les données simulées, le courant normal est d'environ :

2.1 A

Une valeur élevée est utilisée pour simuler une situation anormale :

5.5 A

Exemple :

Temperature : 24.0 °C
Humidity    : 40.0 %
Vibration   : 0.0
Current     : 5.5 A

Le modèle identifie cette observation comme une anomalie.

6. Entraînement du modèle

Le modèle est entraîné avec le script :

data_science/anomaly_detection.py

Les données sont chargées depuis :

data/processed/sensor_data_clean.csv

Le modèle utilisé est :

IsolationForest(
    n_estimators=100,
    contamination="auto",
    random_state=42
)
7. Sauvegarde du modèle

Après l'entraînement, le modèle est sauvegardé avec Joblib :

models/isolation_forest.joblib

Cela permet de réutiliser le modèle sans devoir le réentraîner à chaque nouvelle donnée.

8. Prédiction en temps réel

Le fichier :

data_science/ml_predict.py

permet de charger le modèle sauvegardé et d'effectuer une prédiction sur une nouvelle mesure.

Le fonctionnement est :

Nouvelle donnée IoT
        ↓
Préparation des variables
        ↓
Chargement du modèle
        ↓
Isolation Forest
        ↓
Prediction
        ↓
Anomaly + Anomaly Score
9. Intégration avec MQTT

Lorsqu'une nouvelle mesure arrive depuis l'ESP32 via MQTT, le subscriber Python appelle automatiquement le module de prédiction.

Le flux est :

ESP32
  ↓
MQTT
  ↓
Python Subscriber
  ↓
ml_predict.py
  ↓
Isolation Forest
  ↓
NORMAL / ANOMALY
  ↓
SQLite

Ainsi, chaque nouvelle mesure peut être analysée automatiquement.

10. Résultats obtenus

Lors d'un test avec les données simulées, le dataset contenait :

20 observations

Résultat obtenu :

14 observations normales
6 anomalies

Soit un taux d'anomalies de :

30 %

Les anomalies correspondaient notamment aux observations présentant un courant de :

5.5 A
11. Évaluation

Dans une application industrielle réelle, le modèle devrait être évalué avec des données contenant des anomalies connues.

Lorsque les véritables labels sont disponibles, plusieurs métriques peuvent être utilisées :

Precision
Recall
F1-score
Confusion Matrix

Ces métriques permettent de mesurer la capacité du système à détecter correctement les anomalies.

Dans ce projet de simulation, les anomalies sont principalement générées à des fins de démonstration et de validation du pipeline.

12. Limites

Le modèle actuel utilise des données simulées.

Les principales limites sont :

absence de données industrielles réelles ;
nombre limité d'observations ;
anomalies simulées ;
absence de calibration avec une machine réelle ;
modèle entraîné sur un petit dataset.

Les résultats doivent donc être considérés comme une démonstration technique du pipeline IoT + Data Science + Machine Learning.

13. Améliorations futures

Le projet peut être amélioré avec :

davantage de données ;
données provenant de capteurs physiques ;
PostgreSQL ;
FastAPI ;
Docker ;
Grafana ;
MQTT sécurisé ;
Cloud IoT ;
XGBoost ;
Local Outlier Factor ;
One-Class SVM ;
modèles LSTM pour les séries temporelles ;
système d'alertes automatiques ;
maintenance prédictive.
14. Pipeline Machine Learning complet

Le pipeline final est :

Collecte IoT
     ↓
MQTT
     ↓
Stockage SQLite
     ↓
Nettoyage des données
     ↓
Analyse exploratoire
     ↓
Préparation des features
     ↓
Isolation Forest
     ↓
Détection des anomalies
     ↓
Sauvegarde du modèle
     ↓
Prédiction en temps réel
     ↓
Dashboard Streamlit

Ce pipeline constitue la partie Data Science et Machine Learning du projet IoT de surveillance industrielle.