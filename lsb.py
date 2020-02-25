import numpy as np
import cv2 as cv
import queue

img = cv.imread('img/parrot.png', 0)

# message = input("Type in the message that you would like to be hidden")
message = "ktfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljksmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljks"

binMessage = []

for i in message:
    binMessage.append(format(ord(i), '08b'))

endOfLengthIndicator = '0101010101010101'

binMessageQueue = queue.Queue()
length = format(len(binMessage), '08b')

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
            # print("before" + str(img[i][j]))
            byte = format(img[i][j], 'b')
            # print(byte)
            # print("binMessageQueue" + str(binMessageQueue.get()))
            updatedLastBit = int(byte[-1]) | int(binMessageQueue.get())
            # print(updatedLastBit)
            img[i][j] = int(byte[0:-1] + str(updatedLastBit), 2)
            # print("after" + str(img[i][j]))

if cv.imwrite('stegoImg/parrot.png', img):
    cv.imshow('stegoImage', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

