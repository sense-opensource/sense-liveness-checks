from fastapi import FastAPI, File, UploadFile, Query, Body, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import os
import cv2
import numpy as np
import time
import logging
import base64
from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.deepfake import run_deepfake_model
from utils.utility import parse_model_name
from utils.analyze_metadata import analyze_metadata
from utils.preprocess import preprocess_image, get_exif_data
from utils.visualization import visualize_results
import gc
from datetime import datetime

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sense-image-process")
# Allow CORS (e.g. frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3010"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting (in-memory example)
RATE_LIMIT = {}
MAX_REQUESTS = 10
WINDOW_SECONDS = 60

# liveness model
model_dir = "resources/anti_spoof_models"
device_id = 0
model_test = AntiSpoofPredict(device_id)
image_cropper = CropImage()

@app.post("/liveness")
async def livenss_prediction(
    image: UploadFile = File(None),
    image_url: str = Query(None),
    base64_string: str = Body(None),
):
    try:
        img, exif_data = await preprocess_image(image, image_url, base64_string)
        metadata_issues, metadata_score, analyze_metadata_status = analyze_metadata(exif_data)
        df_label, df_conf = run_deepfake_model(img)
        if not analyze_metadata_status or df_label != "REAL":
        # if df_label != "REAL":
            return JSONResponse({
                "label": "Spoof",
                "confidence":round(float(df_conf), 3),
                "metadata_issues": metadata_issues,
                "stage": "Spoof"
            })
        else: 
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
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/deepfake")
async def deepfake_prediction(
    file: UploadFile = File(None),
    image_url: str = Query(None),
    base64_string: str = Body(None),
):
    try:
        img, exif_data = await preprocess_image(file, image_url, base64_string)
        metadata_issues, metadata_score, analyze_metadata_status = analyze_metadata(exif_data)
        label, confidence = run_deepfake_model(img)
        if not analyze_metadata_status or label != "REAL":
            label = "Deepfake Suspect"
        visualized = visualize_results(img, label, confidence)
        _, buffer = cv2.imencode('.png', visualized)
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        del img, visualized, buffer
        gc.collect()
        return {
            "label": label,
            "confidence": round(float(confidence), 3),
            "metadata_issues": metadata_issues,
            "image_preview": encoded_image,
            "model": ''
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")