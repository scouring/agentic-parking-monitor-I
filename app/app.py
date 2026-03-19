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
from agent_service.agent import run_agent
from PIL import Image
import tempfile

st.title("🚗 Smart Parking Assistant 🚘")

uploaded_file = st.file_uploader("Upload Parking Image")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        image.save(tmp.name, format = "PNG")

        detections = detect_parking(tmp.name)
        stats = count_occupancy(detections)
        agent = run_agent(stats)

    st.subheader("📊 Parking Status")
    st.write(stats)

    st.subheader("🤖 AI Assistant")
    st.success(agent["message"])


