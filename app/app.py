import os
import sys
import streamlit as st
import pandas as pd
from PIL import Image
import tempfile
import time

# Project root for imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from vision_service.detect import detect_parking
from vision_service.occupancy_counter import count_occupancy
from vision_service.logger import log_stats
from agent_service.agent import run_agent

# -------------------------
# Initialize session state df
# -------------------------
if "df" not in st.session_state:
    if os.path.exists("data_log.json"):
        st.session_state.df = pd.read_json("data_log.json", lines=True)
    else:
        st.session_state.df = pd.DataFrame(columns=[
            "timestamp", "occupied", "available", "rate"
        ])

# -------------------------
# App title and uploader
# -------------------------
st.title("🚗 Smart Parking Assistant 🚘")
uploaded_file = st.file_uploader("Upload Parking Image")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        image.save(tmp.name, format="PNG")

        # Run detection and occupancy counting
        detections = detect_parking(tmp.name)
        stats = count_occupancy(detections)

        # Log stats to session state and file
        stats_log = log_stats(stats)

        # Run your agent decision engine
        agent = run_agent(stats)


    # -------------------------
    # Display Metrics
    # -------------------------
    st.subheader("📊 Parking Metrics")
    st.metric("Total Spots", stats["total"])
    st.metric("Occupied", stats["occupied"])
    st.metric("Available", stats["available"])

    occupancy_rate = stats["occupied"] / stats["total"]
    st.progress(occupancy_rate)

    # -------------------------
    # Occupancy Trend Chart (live)
    # -------------------------
    df = st.session_state.df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    st.subheader("📈 Occupancy Trend")
    st.line_chart(df, x="timestamp", y="rate")

    # -------------------------
    # AI Decision Engine
    # -------------------------
    st.subheader("⚙️ AI Decision Engine")
    st.json(agent["decision"])

    st.subheader("🧠 Explanation")
    st.success(agent["message"])