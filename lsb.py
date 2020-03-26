import cv2 as cv
import queue

chosenImg = "parrot.png"

img = cv.imread("img/" + chosenImg, 0)

# type the message that you would like to be hidden
message = "SquirrelsSquirrelsSquirrelsSquirrels"
embedRate = 3

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

