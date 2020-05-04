def lsbExtended(chosenImg, backgroundEmbedRate, weakEmbedRate, strongEmbedRate, message, weakEdgeThreshold, strongEdgeThreshold, thresholdRatio, cv, queue, copy, stegoFunctions):

    img = cv.imread("img/" + chosenImg, 0)
    maskedImg = copy.deepcopy(img)

    bitMask = stegoFunctions.bin_mask_generator(strongEmbedRate)

    # mask the image to the correct embed rate
    for i in range(len(img)):
        for j in range(len(img[0])):
            maskedImg[i][j] = (img[i][j] & bitMask)

    # calculate the edge pixels
    weakEdges = cv.Canny(maskedImg, weakEdgeThreshold, weakEdgeThreshold * thresholdRatio)
    strongEdges = cv.Canny(maskedImg, strongEdgeThreshold, strongEdgeThreshold * thresholdRatio)

    cv.imshow('edges', weakEdges)
    cv.waitKey(0)
    cv.destroyAllWindows()

    cv.imshow('edges', strongEdges)
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
            # if it is a strong edge pixel
            if not binMessageQueue.empty():
                updatedLastBits = ''
                byte = format(img[i][j], '08b')
                if strongEdges[i][j] == 255:
                    for k in range(strongEmbedRate):
                        updatedLastBits += binMessageQueue.get()
                    img[i][j] = int(byte[:-strongEmbedRate] + updatedLastBits, 2)
                elif weakEdges[i][j] == 255:
                    for k in range(weakEmbedRate):
                        updatedLastBits += binMessageQueue.get()
                    img[i][j] = int(byte[:-weakEmbedRate] + updatedLastBits, 2)
                else:
                    for k in range(backgroundEmbedRate):
                        updatedLastBits += binMessageQueue.get()
                    img[i][j] = int(byte[:-backgroundEmbedRate] + updatedLastBits, 2)

    if cv.imwrite("lsbExtended/" + chosenImg, img):
        return True
    else:
        return False
