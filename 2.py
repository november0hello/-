from collections import deque
import os
from PIL import Image
import requests
import sys
import telepot
import time
import cv2
import numpy as np
import math
import pandas as pd

def inc_uses():
    try:
        with open("uses.txt") as f:
            uses = int(f.read().split("\n")[0].strip())
    except:
        uses = 0
    
    with open("uses.txt", "w") as f:
        f.write(str(uses+1))

def resize_image(path):
    img = cv2.imread(path)
    d = 4
    width = int(img.shape[1] / d)
    height = int(img.shape[0] / d)
    dim = (width, height)

    # resize image with box_filter getting I_d picture
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_LINEAR)
    
    # Kernel of the convolution
    conv_kern = np.array([[1 / (16), 2 / (16), 1 / (16)],
                    [2 / (16), 4 / (16), 2 / (16)],
                    [1 / (16), 2 / (16), 1 / (16)]])
    
    # opencv convolution 
    res = cv2.filter2D(resized, -1, conv_kern)

    cv2.imwrite(path + ".png",res)    
    return path + ".png"

def chat_handler(msg):
    msg_type, chat_type, chat_id = telepot.glance(msg)

    if msg_type == "document":
        if "image/png" in msg["document"]["mime_type"] or "image/jpeg" in msg["document"]["mime_type"]:
            file_id = msg["document"]["file_id"]
        else:
            return
    elif msg_type == "photo":
        file_id = msg["photo"][-1]["file_id"]
    else:
        return

    file_path = "downloads/" + bot.getFile(file_id)["file_path"].split("/")[1]
    bot.download_file(file_id, file_path)

    # Resize and send file
    new_file_path = resize_image(file_path)
    with open(new_file_path, "rb") as f:
        bot.sendDocument(chat_id, f)
    
    inc_uses()

    # Clean up working directory
    os.remove(file_path)
    os.remove(new_file_path)

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    bot = telepot.Bot('5669967562:AAHWIKJEHx4z9znW0lROhTjmTVQ-HG2fz58')

    # New message listener
    bot.message_loop({'chat' : chat_handler},
                      run_forever="Bot Running...")