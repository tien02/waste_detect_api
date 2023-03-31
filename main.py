import os, shutil
from PIL import Image
import cv2 as cv
import numpy as np
from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from src import read_img, load_model

model = load_model()
app = FastAPI()

origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {
        "message": "Welcome to Waste detection api"
    }

@app.post('/detect')
async def detection(
    img_file:UploadFile = File(..., description="Upload image file"),
    bb_format: str = Query('xyxy',description="Return bounding box in the chosen format, can be 'xyxy' or 'xywh'"),
    return_image: bool = Query(False, description="Whether return images or just bounding box coordinate"),
    ):
    
    # read image
    # img, img_shape = read_img(image_path=img_file.filename)
    try:
        image = Image.open(img_file.file)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        width, height = image.size
    except:
        raise HTTPException(status_code=500, detail="Something went wrong when reading image")

    # inference
    prediction = model(image)

    if return_image:
        if os.path.exists('runs'):
            shutil.rmtree('runs')
        prediction.save()
        return FileResponse('./runs/detect/exp/image0.jpg')
    
    pred_df = prediction.pandas().xyxy[0]   # pandas dataframe
    if bb_format == 'xywh':
        pred_df = prediction.pandas().xywh[0]   # pandas dataframe

    json_result = {
        'model_predict': pred_df.to_dict('records'),
        'height': height,
        'width': width,
    }

    img_file.file.close()
    image.close()

    return JSONResponse(content=json_result)
