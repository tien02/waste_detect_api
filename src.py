import config
import torch
import numpy as np
import matplotlib.pyplot as plt
from termcolor import colored
import cv2 as cv

def read_img(image_path: str, to_rgb:bool = True, resize:bool = False) -> np.array:
    img = cv.imread(image_path)
    if to_rgb:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    if resize:
        img = cv.resize(img, config.IMG_SIZE, interpolation = cv.INTER_AREA)
    return img

def show_img(image_path:str):
    img = read_img(image_path=image_path)
    plt.axis('off')
    plt.imshow(img)
    plt.show()


def test_read_show_img(test_img_path:str = "demo.jpg"):
    img = read_img(test_img_path)
    if len(img.shape) == 3:
        print(colored("=== PASS ==="), "green")
    else:
        print(colored("=== ERROR ===", "red"))

    show_img(test_img_path)
    
    print(colored("=== PASS ===", "green"))

def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=config.CKPT_PATH, _verbose=False)
    model.conf = config.CONFIDENCE_THRESHOLD
    model.iou = config.IOU_THRESHOLD
    return model

if __name__ == "__main__":
    test_read_show_img()