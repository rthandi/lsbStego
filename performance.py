import cv2 as cv
import numpy as np

chosenImg = "xray.jpeg"

originalImg = cv.imread("img/" + chosenImg, 0)
alteredImg = cv.imread("stegoImg/" + chosenImg, 0)

mse = np.sum((originalImg.astype("float") - alteredImg.astype("float")) ** 2)
mse /= float(originalImg.shape[0] * originalImg.shape[1])

print(mse)