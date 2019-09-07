# http://study.marearts.com/2018/10/dithering-python-opencv-source-code.html

import cv2
import numpy as np
import time


def minmax(v):
    if v > 255:
        v = 255
    if v < 0:
        v = 0
    return v


def dithering_gray(inMat, samplingF):
    inicio = time.time()
    # https://en.wikipedia.org/wiki/Floyd–Steinberg_dithering
    # https://www.youtube.com/watch?v=0L2n8Tg2FwI&t=0s&list=WL&index=151
    # input is supposed as color
    # grab the image dimensions
    h = inMat.shape[0]
    w = inMat.shape[1]

    # loop over the image
    for y in range(0, h - 1):
        for x in range(1, w - 1):
            # threshold the pixel
            old_p = inMat[y, x]
            new_p = np.round(samplingF * old_p / 255.0) * (255 / samplingF)
            inMat[y, x] = new_p

            quant_error_p = old_p - new_p

            # inMat[y, x+1] = minmax(inMat[y, x+1] + quant_error_p * 7 / 16.0)
            # inMat[y+1, x-1] = minmax(inMat[y+1, x-1] + quant_error_p * 3 / 16.0)
            # inMat[y+1, x] = minmax(inMat[y+1, x] + quant_error_p * 5 / 16.0)
            # inMat[y+1, x+1] = minmax(inMat[y+1, x+1] + quant_error_p * 1 / 16.0)

            inMat[y, x + 1] = minmax(inMat[y, x + 1] + quant_error_p * 7 / 16.0)
            inMat[y + 1, x - 1] = minmax(inMat[y + 1, x - 1] + quant_error_p * 3 / 16.0)
            inMat[y + 1, x] = minmax(inMat[y + 1, x] + quant_error_p * 5 / 16.0)
            inMat[y + 1, x + 1] = minmax(inMat[y + 1, x + 1] + quant_error_p * 1 / 16.0)

            #   quant_error  := oldpixel - newpixel
            #   pixel[x + 1][y    ] := pixel[x + 1][y    ] + quant_error * 7 / 16
            #   pixel[x - 1][y + 1] := pixel[x - 1][y + 1] + quant_error * 3 / 16
            #   pixel[x    ][y + 1] := pixel[x    ][y + 1] + quant_error * 5 / 16
            #   pixel[x + 1][y + 1] := pixel[x + 1][y + 1] + quant_error * 1 / 16

    fim = time.time()
    print(fim - inicio)
    # return the thresholded image
    return inMat


def dithering_color(inMat, samplingF):
    inicio = time.time()
    # https://en.wikipedia.org/wiki/Floyd–Steinberg_dithering
    # https://www.youtube.com/watch?v=0L2n8Tg2FwI&t=0s&list=WL&index=151
    # input is supposed as color
    # grab the image dimensions
    h = inMat.shape[0]
    w = inMat.shape[1]

    # loop over the image
    for y in range(0, h - 1):
        for x in range(1, w - 1):
            # threshold the pixel
            old_b = inMat[y, x, 0]
            old_g = inMat[y, x, 1]
            old_r = inMat[y, x, 2]

            new_b = np.round(samplingF * old_b / 255.0) * (255 / samplingF)
            new_g = np.round(samplingF * old_g / 255.0) * (255 / samplingF)
            new_r = np.round(samplingF * old_r / 255.0) * (255 / samplingF)

            inMat[y, x, 0] = new_b
            inMat[y, x, 1] = new_g
            inMat[y, x, 2] = new_r

            quant_error_b = old_b - new_b
            quant_error_g = old_g - new_g
            quant_error_r = old_r - new_r

            inMat[y, x + 1, 0] = minmax(inMat[y, x + 1, 0] + quant_error_b * 7 / 16.0)
            inMat[y, x + 1, 1] = minmax(inMat[y, x + 1, 1] + quant_error_g * 7 / 16.0)
            inMat[y, x + 1, 2] = minmax(inMat[y, x + 1, 2] + quant_error_r * 7 / 16.0)

            inMat[y + 1, x - 1, 0] = minmax(inMat[y + 1, x - 1, 0] + quant_error_b * 3 / 16.0)
            inMat[y + 1, x - 1, 1] = minmax(inMat[y + 1, x - 1, 1] + quant_error_g * 3 / 16.0)
            inMat[y + 1, x - 1, 2] = minmax(inMat[y + 1, x - 1, 2] + quant_error_r * 3 / 16.0)

            inMat[y + 1, x, 0] = minmax(inMat[y + 1, x, 0] + quant_error_b * 5 / 16.0)
            inMat[y + 1, x, 1] = minmax(inMat[y + 1, x, 1] + quant_error_g * 5 / 16.0)
            inMat[y + 1, x, 2] = minmax(inMat[y + 1, x, 2] + quant_error_r * 5 / 16.0)

            inMat[y + 1, x + 1, 0] = minmax(inMat[y + 1, x + 1, 0] + quant_error_b * 1 / 16.0)
            inMat[y + 1, x + 1, 1] = minmax(inMat[y + 1, x + 1, 1] + quant_error_g * 1 / 16.0)
            inMat[y + 1, x + 1, 2] = minmax(inMat[y + 1, x + 1, 2] + quant_error_r * 1 / 16.0)

            #   quant_error  := oldpixel - newpixel
            #   pixel[x + 1][y    ] := pixel[x + 1][y    ] + quant_error * 7 / 16
            #   pixel[x - 1][y + 1] := pixel[x - 1][y + 1] + quant_error * 3 / 16
            #   pixel[x    ][y + 1] := pixel[x    ][y + 1] + quant_error * 5 / 16
            #   pixel[x + 1][y + 1] := pixel[x + 1][y + 1] + quant_error * 1 / 16

    fim = time.time()
    print(fim - inicio)
    # return the thresholded image
    return inMat


img = np.array([[100, 76, 15, 189], [201, 173, 28, 120], [127, 168, 69, 128]], dtype=np.uint8)
new_img = dithering_gray(img, 1)
print(new_img)

# # read image
# inMat = cv2.imread('./../in/baboon.png')  # lena.png')
# # color ditering
# outMat_color = dithering_color(inMat.copy(), 0.5)
# cv2.imwrite('./../out/baboon-color-test-0.5.png', outMat_color)
#
# inMat = cv2.imread('./../in/baboon.png')  # lena.png')
# # color ditering
# outMat_color = dithering_color(inMat.copy(), 0.8)
# cv2.imwrite('./../out/baboon-color-test-0.8.png', outMat_color)
#
# inMat = cv2.imread('./../in/baboon.png')  # lena.png')
# # color ditering
# outMat_color = dithering_color(inMat.copy(), 1)
# cv2.imwrite('./../out/baboon-color-test-1.0.png', outMat_color)
#
# inMat = cv2.imread('./../in/baboon.png')  # lena.png')
# # color ditering
# outMat_color = dithering_color(inMat.copy(), 1.2)
# cv2.imwrite('./../out/baboon-color-test-1.2.png', outMat_color)
#
# inMat = cv2.imread('./../in/baboon.png')  # lena.png')
# # color ditering
# outMat_color = dithering_color(inMat.copy(), 1.5)
# cv2.imwrite('./../out/baboon-color-test-1.5.png', outMat_color)
#
# inMat = cv2.imread('./../in/baboon.png')  # lena.png')
# # color ditering
# outMat_color = dithering_color(inMat.copy(), 1.8)
# cv2.imwrite('./../out/baboon-color-test-1.8.png', outMat_color)
#
# inMat = cv2.imread('./../in/baboon.png')  # lena.png')
# # color ditering
# outMat_color = dithering_color(inMat.copy(), 2)
# cv2.imwrite('./../out/baboon-color-test-2.0.png', outMat_color)
#
# inMat = cv2.imread('./../in/baboon.png')  # lena.png')
# # color ditering
# outMat_color = dithering_color(inMat.copy(), 2.5)
# cv2.imwrite('./../out/baboon-color-test-2.5.png', outMat_color)
#
# inMat = cv2.imread('./../in/baboon.png')  # lena.png')
# # color ditering
# outMat_color = dithering_color(inMat.copy(), 3)
# cv2.imwrite('./../out/baboon-color-test-3.0.png', outMat_color)
#
# # gray ditering
# grayMat = cv2.cvtColor(inMat, cv2.COLOR_BGR2GRAY)
# outMat_gray = dithering_gray(grayMat.copy(), 1)
# cv2.imwrite('./../out/baboon-gray-test.png', outMat_gray)
#
# # gray ditering
# grayMat = cv2.cvtColor(inMat, cv2.COLOR_BGR2GRAY)
# outMat_gray = dithering_gray(grayMat.copy(), 0.9)
# cv2.imwrite('./../out/baboon-gray-test-2.png', outMat_gray)
#
# inMat = cv2.imread('./../in/barcelona.png')
# outMat_color = dithering_color(inMat.copy(), 1)
# cv2.imwrite('./../out/barcelona-color-test.png', outMat_color)
#
# grayMat = cv2.cvtColor(inMat, cv2.COLOR_BGR2GRAY)
# outMat_gray = dithering_gray(grayMat.copy(), 1)
# cv2.imwrite('./../out/barcelona-gray-test.png', outMat_gray)

# 30.82866621017456
# 12.114312887191772
# 44.02041292190552
# 15.29588508605957
