import onnxruntime
import numpy as np
import cv2

deepfake_model_path = "resources/deepfake/efficientnet-b7.onnx"
session = onnxruntime.InferenceSession(deepfake_model_path)

def run_deepfake_model(image: np.ndarray):
    resized = cv2.resize(image, (224, 224)) / 255.0
    tensor = np.expand_dims(np.transpose(resized, (2, 0, 1)), axis=0).astype(np.float32)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    output = session.run([output_name], {input_name: tensor})[0][0][0]
    label = "Deepfake detected" if output > 0.5 else "REAL"
    confidence = output if output > 0.5 else 1 - output
    return label, confidence
