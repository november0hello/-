import os
import requests
import sys
import numpy as np
import math
import pandas as pd
import telepot
from telepot.loop import MessageLoop
import time
import cv2

if not os.path.exists("downloads"):
    os.makedirs("downloads")
Bot = telepot.Bot('5669967562:AAHWIKJEHx4z9znW0lROhTjmTVQ-HG2fz58')

def resize_image(path):
    image = cv2.imread(path)
    d = 4
    width = int(image.shape[1] / d)
    height = int(image.shape[0] / d)
    dim = (width, height)

    resized = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

    conv_kern = np.array([[1 / (16), 2 / (16), 1 / (16)],
                    [2 / (16), 4 / (16), 2 / (16)],
                    [1 / (16), 2 / (16), 1 / (16)]])

    res = cv2.filter2D(resized, -1, conv_kern)
    cv2.imwrite(path + ".png",res)    
    return path + ".png"

def handle(message):
    message_type, chat_type, chat_id = telepot.glance(message)

    if message_type == "document":
        if "image/png" in message["document"]["mime_type"] or "image/jpeg" in message["document"]["mime_type"]:
            file_id = message["document"]["file_id"]
        else:
            return
    elif message_type == "photo":
        file_id = message["photo"][-1]["file_id"]
    else:
        return

    file_path = "downloads/" + Bot.getFile(file_id)["file_path"].split("/")[1]
    Bot.download_file(file_id, file_path)
    new_file_path = resize_image(file_path)
    with open(new_file_path, "rb") as f:
        Bot.sendDocument(chat_id, f)

    os.remove(file_path)
    os.remove(new_file_path)

MessageLoop(Bot, handle).run_forever()   
