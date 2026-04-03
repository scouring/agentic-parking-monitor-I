from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import cv2
import time

from services.frame_service import get_next_frame
from services.yolo_service import run_inference
from services.logging_service import log_stats
from services.forecast_service import forecast_next_hour

from agent_service.agent_runner import run_agent

app = FastAPI(title="Smart Parking Monitor")

latest_stats = {}

def generate_frames():

    global latest_stats

    while True:

        frame_path = get_next_frame()

        result = run_inference(frame_path)

        latest_stats = {
            "total": result["total"],
            "occupied": result["occupied"],
            "empty": result["empty"]
        }

        log_stats(latest_stats)

        # image frame with bounding box
        frame = result["image"]

        # converts the image into JPEG bytes so browsers can display it.
        _, buffer = cv2.imencode(".jpg", frame)

        # Streams the fram with an MJPEG stream. Browser can render this as live video.
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + buffer.tobytes() +
            b'\r\n'
        )

        # controls the frame rate
        time.sleep(10)

# video endpoint. returns the live stream at http://localhost:8000/video
@app.get("/video")
def video_feed():

    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# metrics endpoint. returns JSON data about parking status.
@app.get("/metrics")
def metrics():

    forecast = forecast_next_hour()

    agent = run_agent(latest_stats, forecast)

    return {
        "total": latest_stats["total"],
        "occupied": latest_stats["occupied"],
        "empty": latest_stats["empty"],
        "forecast": forecast,
        "agent": agent["message"]
    }

# Serve your existing frontend at root
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")