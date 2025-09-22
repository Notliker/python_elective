import cv2 as cv
import numpy as np

def equalization(img):
    if img.ndim == 3 and img.shape[2] in (3, 4):
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    if img.dtype != np.uint8:
        img = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX).astype(np.uint8)
    dst = cv.equalizeHist(img)
    return dst