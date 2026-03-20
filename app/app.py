import sys
import os

# Must be first. Get absolute path to project root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

# Debug (leave temporarily)
print("ROOT_DIR:", ROOT_DIR)
print("sys.path[0]:", sys.path[0])

import streamlit as st
from vision_service.detect import detect_parking
from vision_service.occupancy_counter import count_occupancy
from vision_service.logger import log_stats
from agent_service.agent import run_agent
from PIL import Image
import tempfile
import pandas as pd

st.title("🚗 Smart Parking Assistant 🚘")

uploaded_file = st.file_uploader("Upload Parking Image")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        image.save(tmp.name, format = "PNG")

        detections = detect_parking(tmp.name)
        stats = count_occupancy(detections)
        stats_log = log_stats(stats)
        agent = run_agent(stats)

    st.subheader("📊 Parking Metrics")
    st.metric("Total Spots", stats["total"])
    st.metric("Occupied", stats["occupied"])
    st.metric("Available", stats["empty"])

    occupancy_rate = stats["occupied"] / stats["total"]
    st.progress(occupancy_rate)

    df = pd.read_json("data_log.json", lines=True)

    st.subheader("📈 Occupancy Trend")
    st.line_chart(df["occupied"])

    st.subheader("⚙️ AI Decision Engine")

    st.json(agent["decision"])

    st.subheader("🧠 Explanation")
    st.success(agent["message"])


