from fastapi import FastAPI, UploadFile
import shutil
import uuid

from vision_service.detect import detect_parking
from vision_service.occupancy_counter import count_occupancy
from agent_service.agent import run_agent

app = FastAPI()

@app.post("/analyze_parking")

async def analyze(file: UploadFile):

    temp_file = f"temp_{uuid.uuid4()}.jpg"

    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    detections = detect_parking(temp_file)
    stats = count_occupancy(detections)
    agent = run_agent(stats)

    return {
        "detections": detections,
        "stats": stats,
        "agent": agent
    }