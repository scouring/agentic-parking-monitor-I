from ultralytics import YOLO

class ParkingModel:

    def __init__(self, model_path="models/best.pt"):

        self.model = YOLO(model_path)
    
    def predict(self, image_path):
        """
        Returns predictions from YOLOv8.
        """
        results = self.model.predict(image_path, imgsz=640)

        return results
