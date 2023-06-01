import config
import cv2 as cv
import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from helper import load_model

model = load_model()

app = FastAPI()

origins = [
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
    return_image: bool = Query(False, description="Whether response images or json"),
    ):
    
    # Read image
    try:
        image = Image.open(img_file.file)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        width, height = image.size
    except:
        raise HTTPException(status_code=500, detail="Something went wrong when reading image")
    
    # inference
    pred = model.predict(source=image, iou=config.IOU_THRESHOLD, conf=config.CONFIDENCE_THRESHOLD)[0]

    if return_image:
        _, im = cv.imencode('.png', pred.plot())
        headers = {'Content-Disposition': 'inline; filename="test.png"'}
        return Response(im.tobytes() , headers=headers, media_type='image/png')

    bb, acc, label = pred.boxes.xyxy.numpy(), pred.boxes.conf.numpy(), pred.boxes.cls.numpy()
    name = [model.names[int(l)] for l in label]
    values = np.concatenate((bb, np.expand_dims(acc, axis=1), np.expand_dims(name, axis=1)), axis=1)
    keys = ["xmin", "ymin", "xmax", "ymax", "confidence", "class", "name"]
    prediction_result = [dict(zip(keys, val)) for val in values]


    json_result = {
        'model_predict': prediction_result,
        'height': height,
        'width': width,
    }

    img_file.file.close()
    image.close()

    return JSONResponse(content=json_result)