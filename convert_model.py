
from ultralytics import YOLO

# Load the YOLO11 model
model = YOLO("/home/npcai/Desktop/NPC_AI_HavaSavunma/data/chapter1ve2_model/last.pt")

# Export the model to TensorRT format
model.export(format="engine",task=detect)  # creates 'yolo11n.engine'
