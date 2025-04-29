from ultralytics import YOLO


class Chapter2:
    def __init__(self):
        self.model_path = "../data/chapter1ve2_model/last.pt"
        self.model = YOLO(self.model_path)

    def predict(self, frame):
        results = self.model.predict(frame)
        return results

#         # Sonuçları işleme
    def sent_stap(self,frame):
        # Sonuçları işleme
        for result in self.predict(frame):
            boxes = result.boxes.xyxy