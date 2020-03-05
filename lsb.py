import numpy as np
import cv2 as cv
import queue

img = cv.imread('img/parrot.png', 0)

# message = input("Type in the message that you would like to be hidden")
message = "ktfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljks"

binMessage = []

temp = "f"
print(format(ord(temp), '08b'))

for i in message:
    print(i)
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
        if not binMessageQueue.empty():
            byte = format(img[i][j], '08b')
            updatedLastBit = int(binMessageQueue.get())
            img[i][j] = int(byte[0:-1] + str(updatedLastBit), 2)

if cv.imwrite('stegoImg/parrot.png', img):
    cv.imshow('stegoImage', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

