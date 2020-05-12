import os
import cv2 as cv
import numpy as np
import math
import queue
import copy
import stegoFunctions
import string
import random

import lsbBasicEmbed
import lsbEdgeEmbed
import lsbExtendedEmbed
import readLsbBasic
import readLsbEdge
import readLsbExtended

# From https://pythonexamples.org/python-generate-random-string-of-specific-length/
def randStr(N, chars = string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(N))

for filename in os.listdir('imageSet/'):
    img = cv.imread('imageSet/' + filename, 0)
    width, height = img.shape[:2]

    #
    # LSB BASIC RESULTS CODE - ADJUST THE EMBED RATE FOR EACH RUN
    #
    #
    # embedRate = 4
    #
    # #   Max amount of bits that can be put into the image
    # bitCapacity = (width * height * embedRate)
    # byteCapacity = math.floor(bitCapacity/8)
    #
    # message = randStr(byteCapacity)
    #
    # # Calculate the length of the image
    # length = format(len(message), '08b')
    # while len(length) % 8 != 0:
    #     length = '0' + length
    #
    # # take away the length of the length representation from the image and the indicator bits
    # message = message[:-int((len(length)/8) + 16)]
    #
    # # If file is written and the message from reading it is the same then run the analysis and print results
    # if lsbBasicEmbed.lsbBasic(filename, embedRate, message, cv, queue):
    #     mse, psnr = stegoFunctions.performance(filename, "lsbBasic/", np, math, cv)
    #     print(filename + " results basic lsb")
    #     print("capacity: " + str(byteCapacity))
    #     print("mse: " + str(round(mse, 3)))
    #     print("psnr: " + str(round(psnr, 3)))
    #
    # #
    # # EDGE LSB RESULTS CODE
    # #
    #
    # embedRateEdges = 4
    # lowThreshold = 40
    # thresholdRatio = 3
    #
    # maskedImg = copy.deepcopy(img)
    # bitMask = stegoFunctions.bin_mask_generator(embedRateEdges)
    # # mask the image to the correct embed rate
    # for i in range(len(img)):
    #     for j in range(len(img[0])):
    #         maskedImg[i][j] = (img[i][j] & bitMask)
    #
    # edges = cv.Canny(maskedImg, lowThreshold, lowThreshold * thresholdRatio)
    #
    # edgeNumber = np.count_nonzero(edges == 255)
    #
    # bitCapacity = (edgeNumber * embedRateEdges)
    # byteCapacity = math.floor(bitCapacity/8)
    #
    # messageEdges = randStr(byteCapacity)
    #
    # # while len(messageEdges) % embedRateEdges != 0:
    # #     messageEdges = messageEdges[:-1]
    #
    # # Calculate the length of the image
    # length = format(len(messageEdges), '08b')
    # while len(length) % 8 != 0:
    #     length = '0' + length
    #
    # # take away the length of the length representation from the image and the indicator bits
    # messageEdges = messageEdges[:-int((len(length)/8) + 16)]
    #
    # if lsbEdgeEmbed.lsbEdge(filename, embedRateEdges, messageEdges, lowThreshold, thresholdRatio, cv, queue, copy, stegoFunctions):
    #     mse, psnr = stegoFunctions.performance(filename, "lsbEdge/", np, math, cv)
    #     print(filename + " results lsb edge")
    #     print("capacity: " + str(byteCapacity))
    #     print("mse: " + str(round(mse, 3)))
    #     print("psnr: " + str(round(psnr, 3)))

    #
    # EXTENDED EDGE LSB RESULTS CODE
    #

    # backgroundEmbedRate = 2
    # weakEmbedRate = 3
    # strongEmbedRate = 4
    # weakEdgeThreshold = 35
    # strongEdgeThreshold = 50
    # thresholdRatio = 3
    #
    # maskedImg = copy.deepcopy(img)
    # bitMask = stegoFunctions.bin_mask_generator(strongEmbedRate)
    # # mask the image to the correct embed rate
    # for i in range(len(img)):
    #     for j in range(len(img[0])):
    #         maskedImg[i][j] = (img[i][j] & bitMask)
    #
    # weakEdges = cv.Canny(maskedImg, weakEdgeThreshold, weakEdgeThreshold * thresholdRatio)
    # strongEdges = cv.Canny(maskedImg, strongEdgeThreshold, strongEdgeThreshold * thresholdRatio)
    #
    # pixelCount = width * height
    # strongEdgeNumber = np.count_nonzero(strongEdges == 255)
    # weakEdgesNumber = np.count_nonzero(weakEdges == 255)
    #
    # pixelCount -= weakEdgesNumber
    # weakEdgesNumber -= strongEdgeNumber
    #
    # bitCapacity = (pixelCount * backgroundEmbedRate) + (weakEdgesNumber * weakEmbedRate) + (strongEdgeNumber * strongEmbedRate)
    #
    # byteCapacity = math.floor(bitCapacity/8)
    #
    # messageExtendedEdges = randStr(byteCapacity)
    #
    # # Calculate the length of the image
    # length = format(len(messageExtendedEdges), '08b')
    # while len(length) % 8 != 0:
    #     length = '0' + length
    #
    # # take away the length of the length representation from the image and the indicator bits
    # messageEdges = messageExtendedEdges[:-int((len(length)/8) + 16)]
    #
    # if lsbExtendedEmbed.lsbExtended(filename, backgroundEmbedRate, weakEmbedRate, strongEmbedRate, messageExtendedEdges, weakEdgeThreshold, strongEdgeThreshold, thresholdRatio, cv, queue, copy, stegoFunctions):
    #     mse, psnr = stegoFunctions.performance(filename, "lsbEdgeExtended/", np, math, cv)
    #     print(filename + " results lsb edge extended")
    #     print("capacity: " + str(byteCapacity))
    #     print("mse: " + str(round(mse, 3)))
    #     print("psnr: " + str(round(psnr, 3)))

    edges = cv.Canny(img, 40, 120)
    cv.imwrite("lsbEdge/" + filename, edges)








