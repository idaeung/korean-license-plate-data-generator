import random as rnd
from PIL import Image, ImageOps
import cv2
import numpy as np
import imutils

def skewing(img):

    random_angle = rnd.randint(-45, 45)
    skewed_img = img.rotate(random_angle, expand=1)
    fff = Image.new('RGBA', skewed_img.size, (255, 255, 255, 255))
    out = Image.composite(skewed_img, fff, skewed_img)
    out.show()
    return skewed_img
