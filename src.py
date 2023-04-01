import config
import torch
from termcolor import colored
import gdown
import os
from ultralytics import YOLO
import cv2 as cv

def read_img(image_path: str, to_rgb:bool = True, resize:bool = False):
    img = cv.imread(image_path)
    if to_rgb:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    if resize:
        img = cv.resize(img, config.IMG_SIZE, interpolation = cv.INTER_AREA)
    return img, img.shape

def load_model():
    ckpt_path = check_ckpt_file()
    print(colored(f"Loading {config.USE_MODEL}", "blue"))

    if config.USE_MODEL == "YOLOV8":    # Load Yolov8
        model = YOLO(ckpt_path)

    else:   # Load Yolov5
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=ckpt_path, _verbose=False)
        model.conf = config.CONFIDENCE_THRESHOLD
        model.iou = config.IOU_THRESHOLD

    return model

def check_ckpt_file():
    weight_path = "yolov5_weights"
    if config.USE_MODEL == "YOLOV8":
        weight_path = "yolov8_weights" 

    if not os.path.exists(weight_path):
        os.makedirs(weight_path)
    save_path = os.path.join(weight_path, "best.pt")
    if len(os.listdir(weight_path)) == 0:  
        print(colored(f"Downloading best.pt to {weight_path}...", "green"))
        url = 'https://drive.google.com/uc?/export=download&id=' + config.YOLOV5_PATH.split('/')[-2]
        if config.USE_MODEL == "YOLOV8":
            url = 'https://drive.google.com/uc?/export=download&id=' + config.YOLOV8_PATH.split('/')[-2]
        gdown.download(url, save_path, quiet=False)
    else:
        print(colored(f"Find existing ckpt file in {weight_path}", "blue"))
    return save_path