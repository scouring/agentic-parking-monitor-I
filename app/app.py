import os
import sys

# -------------------------
# Fix import path FIRST
# -------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

# -------------------------
# Imports
# -------------------------
import streamlit as st
import pandas as pd
from PIL import Image
import time
from datetime import datetime

from vision_service.detect import detect_parking
from vision_service.occupancy_counter import count_occupancy
from vision_service.logger import log_stats
from agent_service.agent import run_agent
from models.linear_regression import forecast_next_hour

# -------------------------
# Paths (robust for deployment)
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRAME_DIR = os.path.join(BASE_DIR, "..", "dataset", "valid", "images")

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
# Live Feed Simulation
# -------------------------
# FRAME_DIR = "../dataset/valid/images"

def simulate_live_feed(frame_dir, delay=2):
    frames = sorted([
        os.path.join(frame_dir, f)
        for f in os.listdir(frame_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])
    
    for frame in frames:
        yield frame
        time.sleep(delay)

# -------------------------
# App UI
# -------------------------
st.title("🚗 Smart Parking Assistant 🚘")
run_simulation = st.button("▶️ Start Live Feed Simulation")

if run_simulation:
    placeholder = st.empty()
    for frame_path in simulate_live_feed(FRAME_DIR):
        with placeholder.container():
            # -------------------------
            # Image display
            # -------------------------
            image = Image.open(frame_path)
            st.image(image, caption="Live Feed Frame", use_container_width=True)

            # -------------------------
            # Detections + stats
            # -------------------------
            detections = detect_parking(frame_path)
            stats = count_occupancy(detections)

            occupancy_rate = (
                stats["occupied"] / stats["total"]
                if stats["total"] > 0 else 0
            )

            # -------------------------
            # Logging
            # -------------------------
            log_stats(stats)

            new_row = {
                "timestamp": datetime.now(),
                "occupied": stats["occupied"],
                "available": stats["available"],
                "rate": occupancy_rate
            }

            st.session_state.df = pd.concat(
                [st.session_state.df, pd.DataFrame([new_row])],
                ignore_index=True
            )

            # -------------------------
            # Forecast
            # -------------------------
            forecast = forecast_next_hour()
            forecast_value = forecast[0] if forecast else None

            # -------------------------
            # Agent decision
            # -------------------------
            agent = run_agent(stats, forecast_value)

            # st.write(stats)
            # st.success(agent["message"])
        
            # -------------------------
            # Display Metrics
            # -------------------------
            st.subheader("📊 Parking Metrics")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total", stats["total"])
            col2.metric("Occupied", stats["occupied"])
            col3.metric("Available", stats["available"])

            st.metric("Occupancy Rate", f"{occupancy_rate:.0%}")
            st.progress(occupancy_rate)

            # -------------------------
            # Forecast Next Hour
            # -------------------------
            # forecast = forecast_next_hour()

            if forecast:
                pred, ts = forecast
                st.subheader("📅 Next Hour Forecast")
                st.info(f"Predicted occupancy at {ts.strftime('%H:%M')}: {pred}")

            # -------------------------
            # Occupancy Trend Chart (live)
            # -------------------------
            df = st.session_state.df.copy()
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp")

            st.subheader("📈 Occupancy Trend")
            st.line_chart(df, x="timestamp", y="rate")

            # -------------------------
            # Decision Output
            # -------------------------
            st.subheader("⚙️ AI Decision Engine")
            st.json(agent["decision"])

            if agent["decision"].get("alert"):
                st.warning(agent["decision"]["alert"])

            # -------------------------
            # Explanation
            # -------------------------
            st.subheader("🧠 Explanation")
            st.success(agent["message"])

        # Small delay to smooth UI updates
        time.sleep(1)