import config
import os, shutil
from PIL import Image
import numpy as np
from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from src import load_model

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
    bb_format: str = Query('xyxy',description="Return bounding box in the chosen format, can be 'xyxy' or 'xywh'"),
    return_image: bool = Query(False, description="Whether return images or just bounding box coordinate"),
    ):
    
    try:
        image = Image.open(img_file.file)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        width, height = image.size
    except:
        raise HTTPException(status_code=500, detail="Something went wrong when reading image")

    if return_image:
        return {
            "message": "This function hasn't supported yet."
        }
        if os.path.exists('runs'):
            shutil.rmtree('runs')
        prediction.save()
        return FileResponse('./runs/detect/exp/image0.jpg')
    
    if config.USE_MODEL == "YOLOV5":
        # inference
        prediction = model(image)

        pred_df = prediction.pandas().xyxy[0]   # pandas dataframe
        if bb_format == 'xywh':
            pred_df = prediction.pandas().xywh[0]   # pandas dataframe
        prediction_result = pred_df.to_dict('records')
    
    else:
        # inference
        pred = model.predict(source=image)[0]
        bb, acc, label = pred.boxes.xyxy.numpy(), pred.boxes.conf.numpy(), pred.boxes.cls.numpy()
        name = [model.names[int(l)] for l in label]
        values = np.concatenate((bb, np.expand_dims(acc, axis=1), np.expand_dims(label, axis=1), np.expand_dims(name, axis=1)), axis=1)
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