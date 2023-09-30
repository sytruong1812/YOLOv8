import torch
import torchvision.models as models

# Load the PyTorch model
model = models.resnet50(pretrained=True)
model.eval()

# Export to ONNX
dummy_input = torch.randn(1, 3, 224, 224)  # Adjust input shape as needed
onnx_path = "model.onnx"
torch.onnx.export(model, dummy_input, onnx_path)