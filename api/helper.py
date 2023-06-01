import os
import gdown
import config
from termcolor import colored
from ultralytics import YOLO

def load_model():
    ckpt_path = check_ckpt_file()

    model = YOLO(ckpt_path)

    return model

def check_ckpt_file():
    weight_path = "ckpt"

    if not os.path.exists(weight_path):
        os.makedirs(weight_path)
    save_path = os.path.join(weight_path, "model.pt")

    if len(os.listdir(weight_path)) == 0:  
        print(colored(f"Downloading best.pt to {weight_path}...", "green"))

        url = 'https://drive.google.com/uc?/export=download&id=' + config.DRIVE_PATH.split('/')[-2]
        gdown.download(url, save_path, quiet=False)
    else:
        print(colored(f"Find existing ckpt file in {weight_path}", "blue"))
    return save_path