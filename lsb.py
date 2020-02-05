import numpy as np
import cv2 as cv

img = cv.imread('img/parrot.png', 0)

print(img)

# message = input("Type in the message that you would like to be hidden")
message = "hello this is a test"



binMessage = []

for i in message:
    binMessage.append(format(ord(i), '08b'))

print(binMessage)

#need to change loop parameters - currently goes by length of message not the length of the image as it should be
for i in range(0, len(binMessage) - 1):
    for j in range(0, 7):
        byte = format(img[i][j], 'b')
        updatedLastBit = int(byte[-1]) | int(binMessage[i][j])
        print("og image " + str(img[i][j]))
        print(byte[0:-1] + str(updatedLastBit))
        img[i][j] = int(byte[0:-1] + str(updatedLastBit), 2)
        print(img[i][j])

cv.imshow('stegoImage', img)
cv.waitKey(0)
cv.destroyAllWindows()
