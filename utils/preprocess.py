from PIL import Image
from io import BytesIO
import filetype
import cv2
import numpy as np
from fastapi import HTTPException

async def preprocess_image(image, image_url, base64_string):

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
    kind = filetype.guess(contents)
    if not kind or kind.mime.split('/')[0] != 'image':
        raise HTTPException(status_code=400, detail="Invalid image type")
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Image decoding failed")
    exif_data = get_exif_data(contents)
    del contents
    return image, exif_data

def validate_image_type(image_bytes: bytes):
    kind = filetype.guess(image_bytes)
    if not kind or kind.mime.split('/')[0] != 'image':
        raise HTTPException(status_code=400, detail="Invalid image file")

# def read_image_bytes(image_bytes: bytes):
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     if image is None:
#         raise HTTPException(status_code=400, detail="Image decoding failed")
#     return image

def get_exif_data(image_bytes: bytes):
    try:
        pil_img = Image.open(BytesIO(image_bytes))
        return pil_img._getexif()
    except Exception:
        return None
