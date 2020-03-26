import cv2 as cv
import queue

def binMaskGenerator(number):
    if number == 1:
        # return "11111110"
        return 254
    elif number == 2:
        # return "11111100"
        return 252
    elif number == 3:
        # return "11111000"
        return 248
    elif number == 4:
        # return "11110000"
        return 240
    elif number == 5:
        # return "11100000"
        return 224
    elif number == 6:
        # return "11000000"
        return 192
    else:
        return 128
        # return "10000000"

chosenImg = "xray.jpeg"

img = cv.imread("img/" + chosenImg, 0)

# type the message that you would like to be hidden
message = "SquirrelsSquirrelsSquirrelsSquirrels"
embedRate = 1

bitMask = binMaskGenerator(embedRate)

maskedImg = [[0 for i in range(len(img))] for j in range(len(img[0]))]

# mask the image to the correct embed rate
for i in range(len(img)):
    for j in range(len(img[0])):
        maskedImg[i][j] = (img[i][j] & bitMask)

# calculate the edge pixels
edges = cv.Canny(maskedImg, 40, 120)
cv.imshow('stegoImage', edges)
cv.waitKey(0)

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
        if edges[i][j] == 255:
            updatedLastBits = ''
            if not binMessageQueue.empty():
                byte = format(img[i][j], '08b')
                for k in range(embedRate):
                    updatedLastBits += binMessageQueue.get()
                img[i][j] = int(byte[:-embedRate] + updatedLastBits, 2)

if cv.imwrite("stegoImg/" + chosenImg, img):
    cv.imshow('stegoImage', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

