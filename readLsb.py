import numpy as np
import cv2 as cv
import queue

def compareQueue(queue1, queue2):
    return queue1.queue == queue2.queue

img = cv.imread('stegoImg/parrot.png', 0)

lsbQueue = queue.Queue()

# Get the least significant bits of the image
for x in img:
    for y in x:
        yByte = format(y, '08b')
        lsbQueue.put(yByte[-1])

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
        comparisonQueue.put(0)
    else:
        comparisonQueue.put(1)
    past16.put(nextVal)
    lengthStack.put(nextVal)
    flag = not flag

while not compareQueue(past16, comparisonQueue):
    nextVal = lsbQueue.get()
    print (nextVal)
    lengthStack.put(nextVal)
    past16.get()
    past16.put(nextVal)

print("here2")
for i in range(16):
    lengthStack.get()
print("here3")

length = None

while not lengthStack.empty():
    length.append(lengthStack.get())

#reverse string
length = length[::-1]
lengthInt = int(length, 2)
print(lengthInt)

# while compareQueue(pas)