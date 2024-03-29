def readLsbExtended(chosenImg, backgroundEmbedRate, weakEmbedRate, strongEmbedRate, weakEdgeThreshold, strongEdgeThreshold, thresholdRatio, cv, queue, copy, stegoFunctions):
    img = cv.imread("lsbEdgeExtended/" + chosenImg, 0)
    maskedImg = copy.deepcopy(img)

    bitMask = stegoFunctions.bin_mask_generator(strongEmbedRate)

    # mask the image to the correct embed rate
    for i in range(len(img)):
        for j in range(len(img[0])):
            maskedImg[i][j] = (img[i][j] & bitMask)

    # calculate the edge pixels
    weakEdges = cv.Canny(maskedImg, weakEdgeThreshold, weakEdgeThreshold * thresholdRatio)
    strongEdges = cv.Canny(maskedImg, strongEdgeThreshold, strongEdgeThreshold * thresholdRatio)

    lsbQueue = queue.Queue()

    # Get the least significant bits of the image
    for i in range(len(img)):
        for j in range(len(img[0])):
            jByte = format(img[i][j], '08b')
            if strongEdges[i][j] == 255:
                for k in reversed(range(strongEmbedRate)):
                    lsbQueue.put(jByte[-(k+1)])
            elif weakEdges[i][j] == 255:
                for k in reversed(range(weakEmbedRate)):
                    lsbQueue.put(jByte[-(k+1)])
            else:
                for k in reversed(range(backgroundEmbedRate)):
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
            nextVal = lsbQueue.get()
            lengthStack.put(nextVal)
            past16.get()
            past16.put(nextVal)

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

    return outputString
