from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pathlib import Path
from datetime import datetime
import os
import time
import pandas as pd

from vision_service.detect import detect_parking
from vision_service.occupancy_counter import count_occupancy
from agent_service.agent import run_agent
from models.linear_regression import forecast_next_hour

app = FastAPI(title="Smart Parking Monitor")

FRAME_DIR = Path("dataset/valid/images")

frames = sorted([
    str(FRAME_DIR / f)
    for f in os.listdir(FRAME_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])

frame_index = 0
data_log = []

def process_frame(frame_path):

    detections = detect_parking(frame_path)
    stats = count_occupancy(detections)

    forecast = None
    if len(data_log) >= 3:
        forecast = forecast_next_hour()[0]

    agent_decision = run_agent(stats, forecast)

    row = {
        "timestamp": datetime.now(),
        "occupied": stats["occupied"],
        "available": stats["available"],
        "forecast": forecast,
        "agent": str(agent_decision)
    }

    data_log.append(row)


def frame_generator():

    global frame_index

    while True:

        frame_path = frames[frame_index]

        frame_index = (frame_index + 1) % len(frames)

        process_frame(frame_path)

        with open(frame_path, "rb") as f:
            frame_bytes = f.read()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            frame_bytes +
            b"\r\n"
        )

        time.sleep(1)


@app.get("/video")
def video_feed():

    return StreamingResponse(
        frame_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/metrics")
def metrics():

    if not data_log:
        return {
            "total":0,
            "occupied":0,
            "empty":0,
            "forecast":"N/A",
            "agent":"N/A"
        }

    latest = data_log[-1]

    return {
        "total": latest["occupied"] + latest["available"],
        "occupied": latest["occupied"],
        "empty": latest["available"],
        "forecast": latest["forecast"] if latest["forecast"] else "N/A",
        "agent": latest["agent"]
    }


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")