import os, shutil
from fastapi import FastAPI, File, UploadFile, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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
    img = read_img(image_path=img_file.file)

    # inference
    prediction = model(img)

    json_result = prediction.pandas().xyxy[0].to_json(orient="records")
    if bb_format == 'xywh':
        json_result = prediction.pandas().xywh[0].to_json(orient="records")
    
    if return_image:
        if os.path.exists('runs'):
            shutil.rmtree('runs')
        prediction.save()
        return FileResponse('./runs/detect/exp/image0.jpg')

    # return json_result
    return Response(json_result, media_type="application/json")
