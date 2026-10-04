# ============================================================
# STREAMLIT DASHBOARD
# IoT Industrial Machine Monitoring
# ============================================================

import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = (
    BASE_DIR
    / "data"
    / "sensor_data.db"
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="IoT Anomaly Detection",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "🤖 IoT Industrial Machine Monitoring"
)

st.markdown(
    """
    **ESP32 + MQTT + SQLite + Isolation Forest + Streamlit**

    Surveillance industrielle et détection automatique
    des anomalies en temps réel.
    """
)


# ============================================================
# LOAD DATABASE
# ============================================================

@st.cache_data(ttl=5)
def load_data():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    query = """
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
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return df


df = load_data()


# ============================================================
# CHECK DATA
# ============================================================

if df.empty:

    st.warning(
        "Aucune donnée disponible dans SQLite."
    )

    st.stop()


# ============================================================
# REFRESH
# ============================================================

if st.button("🔄 Actualiser les données"):

    st.cache_data.clear()

    st.rerun()


# ============================================================
# STATISTICS
# ============================================================

total_samples = len(df)

normal_samples = int(
    (df["anomaly"] == 0).sum()
)

anomaly_samples = int(
    (df["anomaly"] == 1).sum()
)

anomaly_rate = (
    anomaly_samples / total_samples * 100
)


# ============================================================
# KPI
# ============================================================

st.subheader("📊 System Overview")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Samples",
        total_samples
    )


with col2:

    st.metric(
        "Normal",
        normal_samples
    )


with col3:

    st.metric(
        "Anomalies",
        anomaly_samples
    )


with col4:

    st.metric(
        "Anomaly Rate",
        f"{anomaly_rate:.2f}%"
    )


# ============================================================
# SENSOR STATISTICS
# ============================================================

st.subheader("🌡️ Sensor Statistics")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Temperature",
        f"{df['temperature'].mean():.2f} °C"
    )


with col2:

    st.metric(
        "Humidity",
        f"{df['humidity'].mean():.2f} %"
    )


with col3:

    st.metric(
        "Vibration",
        f"{df['vibration'].mean():.2f}"
    )


with col4:

    st.metric(
        "Current",
        f"{df['current'].mean():.2f} A"
    )


# ============================================================
# SENSOR MONITORING
# ============================================================

st.subheader("📈 Sensor Monitoring")


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🌡️ Temperature",
        "💧 Humidity",
        "📳 Vibration",
        "⚡ Current"
    ]
)


with tab1:

    st.line_chart(
        df["temperature"]
    )


with tab2:

    st.line_chart(
        df["humidity"]
    )


with tab3:

    st.line_chart(
        df["vibration"]
    )


with tab4:

    st.line_chart(
        df["current"]
    )


# ============================================================
# ANOMALIES
# ============================================================

st.subheader("🚨 Detected Anomalies")

anomalies = df[
    df["anomaly"] == 1
].copy()


if anomalies.empty:

    st.success(
        "Aucune anomalie détectée."
    )

else:

    st.warning(
        f"{len(anomalies)} anomalie(s) détectée(s)."
    )

    st.dataframe(
        anomalies[
            [
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
        ],
        use_container_width=True
    )


# ============================================================
# ANOMALY SCORE
# ============================================================

st.subheader("🤖 Isolation Forest Score")

st.line_chart(
    df["anomaly_score"]
)


# ============================================================
# COMPLETE DATA
# ============================================================

st.subheader("📋 Complete Dataset")

st.dataframe(
    df,
    use_container_width=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "IoT Industrial Machine Monitoring | "
    "ESP32 + MQTT + SQLite + Scikit-learn + Streamlit"
)