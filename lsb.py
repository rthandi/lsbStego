import cv2 as cv
import queue
import copy
import stegoFunctions

chosenImg = "xray.png"
embedRate = 2
lowThreshold = 40
thresholdRatio = 3

img = cv.imread("img/" + chosenImg, 0)
maskedImg = copy.deepcopy(img)
maskedImg2 = copy.deepcopy(img)

# type the message that you would like to be hidden
message = "SquirrelsSquirrelsSquirrelsSquirrels"

bitMask = stegoFunctions.bin_mask_generator(embedRate)

# mask the image to the correct embed rate
for i in range(len(img)):
    for j in range(len(img[0])):
        maskedImg[i][j] = (img[i][j] & bitMask)

# calculate the edge pixels
edges = cv.Canny(maskedImg, lowThreshold, lowThreshold * thresholdRatio)

cv.imshow('edges', edges)
cv.waitKey(0)
cv.destroyAllWindows()

binMessage = []

for i in message:
    binMessage.append(format(ord(i), '08b'))

endOfLengthIndicator = '0101010101010101'

binMessageQueue = queue.Queue()
length = format(len(binMessage), '08b')

# make sure it is a multiple of an 8 bit number as this minimises errors from having part of the indicator in the length
while len(length) % 8 != 0:
    length = '0' + length

for i in length:
    binMessageQueue.put(i)

for i in endOfLengthIndicator:
    binMessageQueue.put(i)

for i in binMessage:
    for j in i:
        binMessageQueue.put(j)

for i in range(len(img)):
    for j in range(len(img[0])):
        # if it is an edge pixel
        if edges[i][j] == 255:
            updatedLastBits = ''
            if not binMessageQueue.empty():
                byte = format(img[i][j], '08b')
                for k in range(embedRate):
                    updatedLastBits += binMessageQueue.get()
                img[i][j] = int(byte[:-embedRate] + updatedLastBits, 2)

for i in range(len(img)):
    for j in range(len(img[0])):
        maskedImg2[i][j] = (img[i][j] & bitMask)


if cv.imwrite("stegoImg/" + chosenImg, img):
    cv.imshow('stegoImage', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

