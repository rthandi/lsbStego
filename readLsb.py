import numpy as np
import cv2 as cv
import queue

def compareQueue(queue1, queue2):
    return queue1.queue == queue2.queue

img = cv.imread('stegoImg/parrot.png', 0)

lsbQueue = queue.Queue()

# Get the least significant bits of the image
for i in range(len(img)):
    for j in range(len(img[0])):
        jByte = format(j, '08b')
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
    print(nextVal)
    past16.put(nextVal)
    lengthStack.put(nextVal)
    flag = not flag

print("here1.5")

while not compareQueue(past16, comparisonQueue):
    # print(compareQueue(past16, comparisonQueue))
    nextVal = lsbQueue.get()
    lengthStack.put(nextVal)
    past16.get()
    past16.put(nextVal)

print("here2")
# Size of stack is 16 here for some reason
for i in range(16):
    lengthStack.get()
print("here3")

print(lengthStack.qsize())

length = ''

while not lengthStack.empty():
    # length += lengthStack.get()
    print(lengthStack.get())
    print(lengthStack.empty())

print(length)

#reverse string
length = length[::-1]
lengthInt = int(length, 2)
print(lengthInt)

# while compareQueue(pas)