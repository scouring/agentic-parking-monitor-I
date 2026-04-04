from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import cv2
import time
import threading

from services.frame_service import get_next_frame
from services.yolo_service import run_inference
from services.logging_service import log_stats
from services.forecast_service import forecast_next_hour
from agent_service.agent_runner import run_agent

app = FastAPI(title="Smart Parking Monitor")

# Shared state
latest_stats = {"total":0,"occupied":0,"empty":0}
latest_frame_jpg = None
last_update = 0
UPDATE_INTERVAL = 15

# Background updater: updates stats and frame every UPDATE_INTERVAL
def background_updater():
    global latest_frame_jpg, latest_stats, last_update

    while True:
        frame_path = get_next_frame()
        result = run_inference(frame_path)

        latest_stats.update({
            "total": result["total"],
            "occupied": result["occupied"],
            "empty": result["empty"]
        })

        _, buffer = cv2.imencode(".jpg", result["image"])
        latest_frame_jpg = buffer.tobytes()

        last_update = int(time.time())   # <- single sync point

        log_stats(latest_stats)

        time.sleep(UPDATE_INTERVAL)

# Start background thread
threading.Thread(target=background_updater, daemon=True).start()

# Video feed endpoint
@app.get("/video")
def video_feed():
    def frame_generator():
        global latest_frame_jpg
        last_frame = None
        while True:
            if latest_frame_jpg != last_frame and latest_frame_jpg is not None:
                last_frame = latest_frame_jpg
                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n'
                    + last_frame +
                    b'\r\n'
                )
            time.sleep(0.1)  # small sleep to reduce CPU usage

    return StreamingResponse(
        frame_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# Metrics endpoint
@app.get("/metrics")
def metrics():
    forecast = forecast_next_hour()
    agent = run_agent(latest_stats, forecast)

    return {
        "total": latest_stats["total"],
        "occupied": latest_stats["occupied"],
        "empty": latest_stats["empty"],
        "forecast": forecast,
        "agent": agent["message"],
        "last_update": last_update
    }

# Serve frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")