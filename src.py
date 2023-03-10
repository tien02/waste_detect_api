import config
import torch
import numpy as np
from termcolor import colored
import gdown
import os
import cv2 as cv

def read_img(image_path: str, to_rgb:bool = True, resize:bool = False) -> np.array:
    img = cv.imread(image_path)
    if to_rgb:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    if resize:
        img = cv.resize(img, config.IMG_SIZE, interpolation = cv.INTER_AREA)
    return img, img.shape

def load_model():
    ckpt_path = check_ckpt_file()
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=ckpt_path, _verbose=False)
    model.conf = config.CONFIDENCE_THRESHOLD
    model.iou = config.IOU_THRESHOLD
    return model

def check_ckpt_file():
    if not os.path.exists('weights'):
        os.makedirs('weights')

    if len(os.listdir('weights')) == 0:  
        print(colored("Downloading best.pt to ./weights...", "green"))
        url = 'https://drive.google.com/uc?/export=download&id=' + config.CKPT_DRIVE_PATH.split('/')[-2]
        gdown.download(url, 'weights/best.pt', quiet=False)
    else:
        print(colored("Find existing ckpt file in ./weights", "blue"))
    return "weights/best.pt"