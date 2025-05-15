from PIL import Image
from io import BytesIO
import filetype
import cv2
import numpy as np
from fastapi import HTTPException

def validate_image_type(image_bytes: bytes):
    kind = filetype.guess(image_bytes)
    if not kind or kind.mime.split('/')[0] != 'image':
        raise HTTPException(status_code=400, detail="Invalid image file")

def read_image_bytes(image_bytes: bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Image decoding failed")
    return image

def get_exif_data(image_bytes: bytes):
    try:
        pil_img = Image.open(BytesIO(image_bytes))
        return pil_img._getexif()
    except Exception:
        return None
