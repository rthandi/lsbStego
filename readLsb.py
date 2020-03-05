import numpy as np
import cv2 as cv
import queue
import binascii

def compareQueue(queue1, queue2):
    return queue1.queue == queue2.queue

img = cv.imread('stegoImg/parrot.png', 0)

lsbQueue = queue.Queue()

# Get the least significant bits of the image
for i in range(len(img)):
    for j in range(len(img[0])):
        jByte = format(img[i][j], '08b')
        lsbQueue.put(jByte[-1])

# get length of message
# Instantiate queues
past16 = queue.Queue(maxsize=16)
comparisonQueue = queue.Queue(maxsize=16)
lengthStack = queue.LifoQueue()

flag = True

print("here1")
# The indicator is 16 length so we can fill the first 16 by default
for i in range(16):
    nextVal = lsbQueue.get()
    if flag:
        comparisonQueue.put('0')
    else:
        comparisonQueue.put('1')
    past16.put(nextVal)
    lengthStack.put(nextVal)
    print(nextVal)
    flag = not flag

print("here1.5")

# we do a check here for every byte only as this minimises errors in reading lengths when part of the indicator is in
# the binary string for the length eg. length is 110110101 - the 0101 would trigger the logic of checking the length of
# the indicator and cause incorrect lengths to be read. Now this only happens if the length is 01010101 which is
# unlikely and can have its own specific logic if needed
while not compareQueue(past16, comparisonQueue):
    # read a byte
    for i in range(8):
        nextVal = lsbQueue.get()
        lengthStack.put(nextVal)
        past16.get()
        past16.put(nextVal)
#
# while not compareQueue(past16, comparisonQueue):
#     # print(compareQueue(past16, comparisonQueue))#
#     nextVal = lsbQueue.get()
#     print(nextVal)
#     lengthStack.put(nextVal)
#     past16.get()
#     past16.put(nextVal)

print("here2")
# removes the indicator from the length stack
for i in range(16):
    print(lengthStack.get())
print("here3")

print(lengthStack.qsize())

length = ''

while not lengthStack.empty():
    length += lengthStack.get()

print(length)

#reverse string
length = length[::-1]
lengthInt = int(length, 2)
print(lengthInt)

length = int(length)
stringBuilder = ''

# while length > 0:
#     byteBuffer = ''
#     for i in range(8):
#         length -= 1
#         byteBuffer += lsbQueue.get()
#     stringBuilder += binascii.b2a_qp(byteBuffer)

for i in range(length):
    stringBuilder += lsbQueue.get()

binary_int = int(stringBuilder, 2)
byte_number = binary_int.bit_length() + 7 // 8

binary_array = binary_int.to_bytes(byte_number, "big")
ascii_text = binary_array.decode()

print(ascii_text)

print(stringBuilder)

# while compareQueue(pas)