import tensorrt as trt

# Load the .onnx model
onnx_path = "model.onnx"
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
with open(onnx_path, 'rb') as model_file:
    onnx_data = model_file.read()

# Initialize the TensorRT engine
trt_engine = trt.Builder(TRT_LOGGER).build_engine(network, max_batch_size=1, max_workspace_size=1 << 30)

# Save the TensorRT engine to a file
trt_path = "model.trt"
with open(trt_path, 'wb') as trt_model_file:
    trt_model_file.write(trt_engine.serialize())