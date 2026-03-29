from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from datetime import datetime
import os
import pandas as pd

from vision_service.detect import detect_parking
from vision_service.occupancy_counter import count_occupancy
from agent_service.agent import run_agent
from models.linear_regression import forecast_next_hour

app = FastAPI(title="Smart Parking Monitor API")

# --- FRAME SETUP ---
FRAME_DIR = Path("dataset/valid/images")
frames = sorted([str(FRAME_DIR / f) for f in os.listdir(FRAME_DIR)
                 if f.lower().endswith((".png", ".jpg", ".jpeg"))])

frame_index = 0
data_log = []

# --- PROCESS ONE FRAME ---
def process_frame(frame_path):
    detections = detect_parking(frame_path)
    stats = count_occupancy(detections)
    occupancy_rate = stats["occupied"] / stats["total"] if stats["total"] else 0

    row = {
        "timestamp": datetime.now(),
        "occupied": stats["occupied"],
        "available": stats["available"],
        "rate": occupancy_rate
    }
    data_log.append(row)
    df = pd.DataFrame(data_log)

    forecast_value = None
    if len(df) >= 3:
        forecast_value = forecast_next_hour()[0]

    agent_decision = run_agent(stats, forecast_value)

    return {
        "frame": frame_path,
        "stats": stats,
        "occupancy_rate": occupancy_rate,
        "forecast": forecast_value,
        "agent": agent_decision
    }

# --- LIVE IMAGE ---
@app.get("/frame_image")
def frame_image():
    global frame_index
    frame_path = frames[frame_index]
    # Increment for next request
    frame_index = (frame_index + 1) % len(frames)
    # Process stats in background
    process_frame(frame_path)
    return FileResponse(frame_path)

# --- METRICS ---
@app.get("/metrics")
def get_metrics():
    if not data_log:
        return {"total": 0, "occupied": 0, "empty": 0}
    latest = data_log[-1]
    return {
        "total": latest["occupied"] + latest["available"],
        "occupied": latest["occupied"],
        "empty": latest["available"]
    }

# --- TREND / HISTORY ---
@app.get("/trend")
def get_trend():
    if not data_log:
        return []
    df = pd.DataFrame(data_log)
    df["timestamp"] = df["timestamp"].astype(str)
    return df.to_dict(orient="records")

# --- STATIC FRONTEND ---
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")