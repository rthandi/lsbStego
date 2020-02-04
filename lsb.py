import numpy as np
import cv2

img = cv2.imread('img/parrot.png')
grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

message = input("Type in the message that you would like to be hidden")

binMessage = []

for i in message:
    binMessage.append(format(ord(i), '08b'))

print(binMessage)

for i in range(0, len(binMessage) - 1):
    for j in range(0, 7):
        print(grayImg[i][j])
        print(binMessage[i][j])
        byte = grayImg[i][j]
        print(byte & ~1)
        updatedByte = (byte & ~1) | binMessage[i][j]
        # grayImg[i][j] = int(updatedByte, 2)
        # bin((grayImg[i*j] & ~1) | binMessage[i][j])

print(grayImg[100, 100])