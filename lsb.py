import cv2 as cv
import queue
import copy
import stegoFunctions

chosenImg = "xray.jpeg"
embedRate = 2

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
edges = cv.Canny(maskedImg, 40, 120)

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
                print("first " + str(img[i][j]))
                img[i][j] = int(byte[:-embedRate] + updatedLastBits, 2)
                print("sec " + str(img[i][j]))

for i in range(len(img)):
    for j in range(len(img[0])):
        maskedImg2[i][j] = (img[i][j] & bitMask)

edges2 = cv.Canny(maskedImg2, 40, 120)

edges2[1][1] = 5

# for i in range(len(maskedImg)):
#     for j in range(len(maskedImg[0])):
#         if edges[i][j] != edges2[i][j]:
#             print("Aofnjasdfnjanjlfknasfnosajdfnba;dsfdnsaljfnsadlfndsafjdsa")

if cv.imwrite("stegoImg/" + chosenImg, img):
    cv.imshow('stegoImage', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

img = cv.imread("stegoImg/" + chosenImg, 0)
maskedImg3 = copy.deepcopy(img)

bitMask = stegoFunctions.bin_mask_generator(embedRate)

# mask the image to the correct embed rate
for i in range(len(img)):
    for j in range(len(img[0])):
        maskedImg3[i][j] = (img[i][j] & bitMask)

# calculate the edge pixels
edges3 = cv.Canny(maskedImg3, 40, 120)
cv.imshow('stegoImage', edges)
cv.waitKey(0)

for i in range(len(img)):
    for j in range(len(img[0])):
        if edges3[i][j] != edges[i][j]:
            # print("new " + str(edges3[i][j]))
            # print("old " + str(edges[i][j]))
            print("FAIL i: " + str(i) + " j: " + str(j))
        elif edges3[i][j] == 255:
            print("PASS i: " + str(i) + " j: " + str(j))




lsbQueue = queue.Queue()

# Get the least significant bits of the image
for i in range(len(img)):
    for j in range(len(img[0])):
        if edges[i][j] == 255:
            jByte = format(img[i][j], '08b')
            for k in reversed(range(embedRate)):
                lsbQueue.put(jByte[-(k+1)])

# get length of message
# Instantiate queues
past16 = queue.Queue(maxsize=16)
comparisonQueue = queue.Queue(maxsize=16)
lengthStack = queue.LifoQueue()

flag = True

# The indicator is 16 length so we can fill the first 16 by default
for i in range(16):
    nextVal = lsbQueue.get()
    if flag:
        comparisonQueue.put('0')
    else:
        comparisonQueue.put('1')
    past16.put(nextVal)
    lengthStack.put(nextVal)
    flag = not flag

# we do a check here for every byte only as this minimises errors in reading lengths when part of the indicator is in
# the binary string for the length eg. length is 110110101 - the 0101 would trigger the logic of checking the length of
# the indicator and cause incorrect lengths to be read. Now this only happens if the length is 01010101 which is
# unlikely and can have its own specific logic if needed
while not stegoFunctions.compare_queue(past16, comparisonQueue):
    # read a byte
    for i in range(8):
        print("here")
        nextVal = lsbQueue.get()
        lengthStack.put(nextVal)
        past16.get()
        past16.put(nextVal)

print("here again")

# removes the indicator from the length stack
for i in range(16):
    lengthStack.get()

length = ''

while not lengthStack.empty():
    length += lengthStack.get()

#reverse string
length = length[::-1]
lengthInt = int(length, 2)

tempArray = []

# extract all of the bytes individually
while lengthInt > 0:
    stringBuilder = ''
    for i in range(8):
        stringBuilder += lsbQueue.get()
    tempArray.append(stringBuilder)
    lengthInt -= 1

outputString = ''

# Convert each byte to its ascii value
for i in tempArray:
    n = int('0b' + i, 2)
    n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    outputString += str(chr(n))



