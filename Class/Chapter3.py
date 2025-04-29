from ultralytics import YOLO


class Chapter3:
    def __init__(self):
        self.model_name = "Chapter1"
        self.model_path = "../data/chapter1_model/last.pt"
        self.model = YOLO(self.model_path)

    def predict(self, frame):
        results = self.model.predict(frame)
        return results
