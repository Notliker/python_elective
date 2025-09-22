import cv2 as cv
import numpy as np

def gamma_correction(img, alpha = 2.0, beta = 30):
    return cv.convertScaleAbs(img, alpha=alpha, beta=beta)