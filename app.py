from fastapi import FastAPI, File, UploadFile, Query, Body, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import cv2
import numpy as np
import time
import logging
from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name
from src.deepfake import run_deepfake_model
from src.analyze_metadata import analyze_metadata
from src.preprocess import validate_image_type, read_image_bytes, get_exif_data


app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sense-image-process")
# Allow CORS (e.g. frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5000",  # Alternative Vite port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# liveness model
model_dir = "resources/anti_spoof_models"
device_id = 0
model_test = AntiSpoofPredict(device_id)
image_cropper = CropImage()

@app.post("/liveness")
async def predict_image(
    image: UploadFile = File(None),
    image_url: str = Query(None),
    base64_string: str = Body(None),
    deepfake_model_name: str = Query("default")
):
    try:
        # Priority 1: File upload
        if image:
            contents = await image.read()
        # Priority 2: S3 URL
        elif image_url:
            try:
                response = requests.get(image_url, timeout=5)
                if response.status_code != 200:
                    raise HTTPException(status_code=400, detail="Failed to download image from URL.")
                contents = response.content
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error downloading image: {str(e)}")
        # Priority 3: Base64 string
        elif base64_string:
            try:
                contents = base64.b64decode(base64_string)
            except Exception as e:
                raise HTTPException(status_code=400, detail="Invalid base64 string")
        else:
            raise HTTPException(status_code=400, detail="No image source provided")
                #image_bytes = await image.read()
        validate_image_type(contents)
        
        img = read_image_bytes(contents)
        exif_data = get_exif_data(contents)
        #metadata_issues, _, _ = analyze_metadata(exif_data)
        metadata_issues, metadata_score, analyze_metadata_status = analyze_metadata(exif_data)
        
        df_label, df_conf = run_deepfake_model(img)
        print(df_label, analyze_metadata_status)
        #if not analyze_metadata_status or df_label != "REAL":
        if df_label != "REAL":
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
