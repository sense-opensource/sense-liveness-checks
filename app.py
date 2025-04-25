from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import cv2
import numpy as np
import time

from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name

app = FastAPI()

# Allow CORS (e.g. frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_dir = "./resources/anti_spoof_models"
device_id = 0
model_test = AntiSpoofPredict(device_id)
image_cropper = CropImage()

@app.post("/liveness")
async def predict(image: UploadFile = File(...)):
    if image.content_type.split("/")[0] != "image":
        raise HTTPException(status_code=400, detail="Invalid file type")

    image_bytes = await image.read()
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    try:
        image_bbox = model_test.get_bbox(img)
    except Exception:
        raise HTTPException(status_code=400, detail="No face detected")

    prediction = np.zeros((1, 3))
    test_speed = 0

    for model_name in os.listdir(model_dir):
        h_input, w_input, model_type, scale = parse_model_name(model_name)
        param = {
            "org_img": img,
            "bbox": image_bbox,
            "scale": scale,
            "out_w": w_input,
            "out_h": h_input,
            "crop": True,
        }
        if scale is None:
            param["crop"] = False

        cropped_img = image_cropper.crop(**param)
        start = time.time()
        prediction += model_test.predict(cropped_img, os.path.join(model_dir, model_name))
        test_speed += time.time() - start

    label = np.argmax(prediction)
    value = float(prediction[0][label] / 2)
    label_text = "Real" if label == 1 else "Spoof"

    return JSONResponse(content={
        "label": label_text,
        "confidence": value
    })
