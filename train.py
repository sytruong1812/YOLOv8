from ultralytics import YOLO
import torch.optim as optim

# Load a model
# model = YOLO('yolov8n.yaml')  # build a new model from YAML
model = YOLO('best.pt')  # load a pretrained model (recommended for training)

if __name__ == '__main__':
    # Train the model
    results = model.train(data='dataset.yaml', epochs=100, imgsz=640, batch=16, workers=5, optimizer='AdamW')
    metrics = model.val()
