from vision_service.model_loader import ParkingModel

model = ParkingModel("models/best.pt")

def detect_parking(image_path):

    results = model.predict(image_path)

    detections = []

    for det in results[0].boxes.data.cpu().numpy():
        # det format: x1, y1, x2, y2, confidence, class

        detections.append({
            "bbox": det[:4].tolist(),
            "confidence": float(det[4]),
            "class": int(det[5])
        })

    return detections