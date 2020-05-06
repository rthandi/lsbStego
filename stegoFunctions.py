def bin_mask_generator(number):
    if number == 1:
        # 254 = 11111110
        return 254
    elif number == 2:
        # 252 = 11111100
        return 252
    elif number == 3:
        # 248 = 11111000
        return 248
    elif number == 4:
        # 240 = 11110000
        return 240
    elif number == 5:
        # 224 = 11100000
        return 224
    elif number == 6:
        # 192 = 11000000
        return 192
    else:
        # 218 = 10000000
        return 128


def compare_queue(queue1, queue2):
    return queue1.queue == queue2.queue

def performance(fileName, resultDirectory, np, math, cv):
    originalImg = cv.imread("imageSet/" + fileName, 0)
    alteredImg = cv.imread(resultDirectory + fileName, 0)


    # Compute mean squared error with: https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
    mse = np.sum((originalImg.astype("float") - alteredImg.astype("float")) ** 2)
    mse /= float(originalImg.shape[0] * originalImg.shape[1])

    # Compute peak signal to noise ratio with:
    PIXEL_MAX = 255.0
    if mse == 0:
        psnr = 100
    else:
        psnr = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

    return mse, psnr
