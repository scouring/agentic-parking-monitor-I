import cv2
from ultralytics import YOLO

model = YOLO("models/best.pt")

def run_inference(frame_path):

    results = model(frame_path)

    boxes = results[0].boxes.cls.tolist()

    occupied = 0
    empty = 0

    for cls in boxes:
        if int(cls) == 0:
            empty += 1
        else:
            occupied += 1

    total = occupied + empty

    annotated = results[0].plot()

    return {
        "occupied": occupied,
        "empty": empty,
        "total": total,
        "image": annotated
    }