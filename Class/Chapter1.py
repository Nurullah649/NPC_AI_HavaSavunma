from ultralytics import YOLO


class Chapter1:
    def __init__(self):
        self.model_path = "/home/nurullah/NPC-AI_HavaSavunma/data/chapter1ve2_model/last.pt"
        self.model = YOLO(self.model_path)

    def predict(self, frame):
        results = self.model.predict(frame, conf=0.5)
        return results

