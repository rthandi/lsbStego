import cv2 as cv
import numpy as np
import math
import matplotlib.pyplot as plt


chosenImg = "xray.jpeg"

originalImg = cv.imread("img/" + chosenImg, 0)
alteredImg = cv.imread("stegoImg/" + chosenImg, 0)

# Compute mean squared error with: https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
mse = np.sum((originalImg.astype("float") - alteredImg.astype("float")) ** 2)
mse /= float(originalImg.shape[0] * originalImg.shape[1])

# Compute peak signal to noise ratio with:
PIXEL_MAX = 255.0
if mse == 0:
    psnr = 100
else:
    psnr = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

# Display the images and results from: https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
# setup the figure
fig = plt.figure(chosenImg)
plt.suptitle("MSE: %.2f, PSNR: %.2f" % (mse, psnr))
# show first image
ax = fig.add_subplot(1, 2, 1)
plt.imshow(originalImg, cmap = plt.cm.gray)
plt.axis("off")
# show the second image
ax = fig.add_subplot(1, 2, 2)
plt.imshow(alteredImg, cmap = plt.cm.gray)
plt.axis("off")
# show the images
plt.show()