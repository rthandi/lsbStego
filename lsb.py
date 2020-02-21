import numpy as np
import cv2 as cv

img = cv.imread('img/parrot.png', 0)

# message = input("Type in the message that you would like to be hidden")
message = "kmfa testasdasdasdasfasf;kmflksdlkjfalksjgkjlsadglkjsdjgsdjkgsjdgjdsglkjdsjkgsdkjgsdjlkgskdjgsdkjgjkdsgljksdgljks"

binMessage = []
binMessageTemp = []

for i in message:
    binMessageTemp.append(format(ord(i), '08b'))

endOfLengthIndicator = '0101010101010101'
#also need end of message indicator

binMessage.append(format(len(binMessageTemp), '08b'))
binMessage.append(endOfLengthIndicator)
print(binMessage)
# extend used so it adds each array item as a separate element not as one big array
binMessage.extend(binMessageTemp)
print(binMessage)

#need to change loop parameters - currently goes by length of message not the length of the image as it should be
for i in range(0, len(binMessage) - 1):
    for j in range(0, 7):
        byte = format(img[i][j], 'b')
        updatedLastBit = int(byte[-1]) | int(binMessage[i][j])
        img[i][j] = int(byte[0:-1] + str(updatedLastBit), 2)

if cv.imwrite('stegoImg/parrot.png', img):
    cv.imshow('stegoImage', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

