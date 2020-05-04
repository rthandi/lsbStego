import os
import cv2 as cv
import queue
import copy
import stegoFunctions


import lsbBasic
import lsbEdge
import lsbExtended
import readLsbBasic
import readLsbEdge
import readLsbExtended

for filename in os.listdir('imageSet/'):
    img = cv.imread(filename, 0)
    width, height = img.shape[:2]
    

