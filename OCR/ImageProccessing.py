import numpy as np
import cv2

class ImageProccessing:
    def __init__(self):
        pass

    @staticmethod
    def Interpolation(image, fx, fy):
        return cv2.resize(image, None, fx = fx, fy = fy, interpolation = cv2.INTER_CUBIC)

    @staticmethod
    def increase_brightness(img, value=30):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    @staticmethod
    def Thresholding_By_HSV(image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        brightness = int(hsv[...,2].mean())
        lower_black = np.array([0, 0, 0], dtype = "uint8")
        upper_black = np.array([0, 0, brightness-23], dtype = "uint8")
        mask = cv2.inRange(hsv, lower_black, upper_black)
        return mask 
        