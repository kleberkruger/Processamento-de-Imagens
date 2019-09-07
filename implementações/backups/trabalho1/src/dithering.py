import cv2
import numpy as np
import time
from math import floor


def imprimir(matriz, y, x):
    print(matriz[y][x], end=" ")


def apply_threshold(self, value):
    return 255 * floor(value / 128)


def floyd_steinberg(img, alternate=True):
    inicio = time.time()
    fim = time.time()
    print(fim - inicio)

    return img


def minmax(v):
    return 0 if v < 0 else 255 if v > 255 else v


def floyd_steinberg_gray(inMat, zigZag=True, samplingF=1):
    pad_y = pad_x = 1
    # TODO: Precisa mesmo colocar borda em cima?
    inMat = cv2.copyMakeBorder(inMat, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)

    for y in range(pad_y, inMat.shape[0] - pad_y):
        for x in range(*(pad_x, inMat.shape[1] - pad_x) if not zigZag or (y - pad_y) % 2 == 0 else (
                inMat.shape[1] - pad_x - 1, pad_x - 1, -1)):
            old_p = inMat[y, x]
            # new_p = 0 if old_p < 128 else 255
            new_p = np.round(samplingF * old_p / 255.0) * (255 / samplingF)
            inMat[y, x] = new_p
            quant_error_p = old_p - new_p

            inMat[y, x + 1] = minmax(inMat[y, x + 1] + quant_error_p * 7 / 16.0)
            inMat[y + 1, x - 1] = minmax(inMat[y + 1, x - 1] + quant_error_p * 3 / 16.0)
            inMat[y + 1, x] = minmax(inMat[y + 1, x] + quant_error_p * 5 / 16.0)
            inMat[y + 1, x + 1] = minmax(inMat[y + 1, x + 1] + quant_error_p * 1 / 16.0)

    return inMat[pad_y:inMat.shape[0] - pad_y, pad_x:inMat.shape[1] - pad_x]


def floyd_steinberg_color(inMat, zigZag=False, samplingF=1):
    pad_y = pad_x = 1
    # TODO: Precisa mesmo colocar borda em cima?
    inMat = cv2.copyMakeBorder(inMat, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)

    for y in range(pad_y, inMat.shape[0] - pad_y):
        for x in range(*(pad_x, inMat.shape[1] - pad_x) if not zigZag or (y - pad_y) % 2 == 0 else (
                inMat.shape[1] - pad_x - 1, pad_x - 1, -1)):
            old_b = inMat[y, x, 0]
            old_g = inMat[y, x, 1]
            old_r = inMat[y, x, 2]

            # new_b = 0 if old_b < 128 else 255
            # new_g = 0 if old_g < 128 else 255
            # new_r = 0 if old_r < 128 else 255
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

    return inMat[pad_y:inMat.shape[0] - pad_y, pad_x:inMat.shape[1] - pad_x]


def stevenson_arce_gray(inMat, zigZag=True, samplingF=1):
    pad_y = pad_x = 3
    inMat = cv2.copyMakeBorder(inMat, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)

    for y in range(pad_y, inMat.shape[0] - pad_y):
        for x in range(*(pad_x, inMat.shape[1] - pad_x) if not zigZag or (y - pad_y) % 2 == 0 else (
                inMat.shape[1] - pad_x - 1, pad_x - 1, -1)):
            old_p = inMat[y, x]
            new_p = np.round(samplingF * old_p / 255.0) * (255 / samplingF)
            inMat[y, x] = new_p
            quant_error_p = old_p - new_p

            inMat[y, x + 2] = minmax(inMat[y, x + 2] + quant_error_p * 32 / 200)
            inMat[y + 1, x - 3] = minmax(inMat[y + 1, x - 3] + quant_error_p * 12 / 200)
            inMat[y + 1, x - 1] = minmax(inMat[y + 1, x - 1] + quant_error_p * 26 / 200)
            inMat[y + 1, x + 1] = minmax(inMat[y + 1, x + 1] + quant_error_p * 30 / 200)
            inMat[y + 1, x + 3] = minmax(inMat[y + 1, x + 3] + quant_error_p * 16 / 200)
            inMat[y + 2, x - 2] = minmax(inMat[y + 2, x + 2] + quant_error_p * 12 / 200)
            inMat[y + 2, x] = minmax(inMat[y + 2, x] + quant_error_p * 26 / 200)
            inMat[y + 2, x + 2] = minmax(inMat[y + 2, x + 2] + quant_error_p * 12 / 200)
            inMat[y + 3, x - 3] = minmax(inMat[y + 3, x - 3] + quant_error_p * 5 / 200)
            inMat[y + 3, x - 1] = minmax(inMat[y + 3, x - 1] + quant_error_p * 12 / 200)
            inMat[y + 3, x + 1] = minmax(inMat[y + 3, x + 1] + quant_error_p * 12 / 200)
            inMat[y + 3, x + 3] = minmax(inMat[y + 3, x + 3] + quant_error_p * 5 / 200)

    return inMat[pad_y:inMat.shape[0] - pad_y, pad_x:inMat.shape[1] - pad_x]


def stevenson_arce_color(inMat, zigZag=False, samplingF=1):
    pad_y = pad_x = 3
    inMat = cv2.copyMakeBorder(inMat, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)

    for y in range(pad_y, inMat.shape[0] - pad_y):
        for x in range(*(pad_x, inMat.shape[1] - pad_x) if not zigZag or (y - pad_y) % 2 == 0 else (
                inMat.shape[1] - pad_x - 1, pad_x - 1, -1)):
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

            inMat[y, x + 2, 0] = minmax(inMat[y, x + 2, 0] + quant_error_b * 32 / 200)
            inMat[y, x + 2, 1] = minmax(inMat[y, x + 2, 1] + quant_error_g * 32 / 200)
            inMat[y, x + 2, 2] = minmax(inMat[y, x + 2, 2] + quant_error_r * 32 / 200)

            inMat[y + 1, x - 3, 0] = minmax(inMat[y + 1, x - 3, 0] + quant_error_b * 12 / 200)
            inMat[y + 1, x - 3, 1] = minmax(inMat[y + 1, x - 3, 1] + quant_error_g * 12 / 200)
            inMat[y + 1, x - 3, 2] = minmax(inMat[y + 1, x - 3, 2] + quant_error_r * 12 / 200)

            inMat[y + 1, x - 1, 0] = minmax(inMat[y + 1, x - 1, 0] + quant_error_b * 26 / 200)
            inMat[y + 1, x - 1, 1] = minmax(inMat[y + 1, x - 1, 1] + quant_error_g * 26 / 200)
            inMat[y + 1, x - 1, 2] = minmax(inMat[y + 1, x - 1, 2] + quant_error_r * 26 / 200)

            inMat[y + 1, x + 1, 0] = minmax(inMat[y + 1, x + 1, 0] + quant_error_b * 30 / 200)
            inMat[y + 1, x + 1, 1] = minmax(inMat[y + 1, x + 1, 1] + quant_error_g * 30 / 200)
            inMat[y + 1, x + 1, 2] = minmax(inMat[y + 1, x + 1, 2] + quant_error_r * 30 / 200)

            inMat[y + 1, x + 3, 0] = minmax(inMat[y + 1, x + 3, 0] + quant_error_b * 16 / 200)
            inMat[y + 1, x + 3, 1] = minmax(inMat[y + 1, x + 3, 1] + quant_error_g * 16 / 200)
            inMat[y + 1, x + 3, 2] = minmax(inMat[y + 1, x + 3, 2] + quant_error_r * 16 / 200)

            inMat[y + 2, x - 2, 0] = minmax(inMat[y + 2, x + 2, 0] + quant_error_b * 12 / 200)
            inMat[y + 2, x - 2, 1] = minmax(inMat[y + 2, x + 2, 1] + quant_error_g * 12 / 200)
            inMat[y + 2, x - 2, 2] = minmax(inMat[y + 2, x + 2, 2] + quant_error_r * 12 / 200)

            inMat[y + 2, x, 0] = minmax(inMat[y + 2, x, 0] + quant_error_b * 26 / 200)
            inMat[y + 2, x, 1] = minmax(inMat[y + 2, x, 1] + quant_error_g * 26 / 200)
            inMat[y + 2, x, 2] = minmax(inMat[y + 2, x, 2] + quant_error_r * 26 / 200)

            inMat[y + 2, x + 2, 0] = minmax(inMat[y + 2, x + 2, 0] + quant_error_b * 12 / 200)
            inMat[y + 2, x + 2, 1] = minmax(inMat[y + 2, x + 2, 1] + quant_error_g * 12 / 200)
            inMat[y + 2, x + 2, 2] = minmax(inMat[y + 2, x + 2, 2] + quant_error_r * 12 / 200)

            inMat[y + 3, x - 3, 0] = minmax(inMat[y + 3, x - 3, 0] + quant_error_b * 5 / 200)
            inMat[y + 3, x - 3, 1] = minmax(inMat[y + 3, x - 3, 1] + quant_error_g * 5 / 200)
            inMat[y + 3, x - 3, 2] = minmax(inMat[y + 3, x - 3, 2] + quant_error_r * 5 / 200)

            inMat[y + 3, x - 1, 0] = minmax(inMat[y + 3, x - 1, 0] + quant_error_b * 12 / 200)
            inMat[y + 3, x - 1, 1] = minmax(inMat[y + 3, x - 1, 1] + quant_error_g * 12 / 200)
            inMat[y + 3, x - 1, 2] = minmax(inMat[y + 3, x - 1, 2] + quant_error_r * 12 / 200)

            inMat[y + 3, x + 1, 0] = minmax(inMat[y + 3, x + 1, 0] + quant_error_b * 12 / 200)
            inMat[y + 3, x + 1, 1] = minmax(inMat[y + 3, x + 1, 1] + quant_error_g * 12 / 200)
            inMat[y + 3, x + 1, 2] = minmax(inMat[y + 3, x + 1, 2] + quant_error_r * 12 / 200)

            inMat[y + 3, x + 3, 0] = minmax(inMat[y + 3, x + 3, 0] + quant_error_b * 5 / 200)
            inMat[y + 3, x + 3, 1] = minmax(inMat[y + 3, x + 3, 1] + quant_error_g * 5 / 200)
            inMat[y + 3, x + 3, 2] = minmax(inMat[y + 3, x + 3, 2] + quant_error_r * 5 / 200)

    return inMat[pad_y:inMat.shape[0] - pad_y, pad_x:inMat.shape[1] - pad_x]


def burkes_gray(inMat, zigZag=True, samplingF=1):
    pad_y = 1
    pad_x = 2
    inMat = cv2.copyMakeBorder(inMat, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)

    for y in range(pad_y, inMat.shape[0] - pad_y):
        for x in range(*(pad_x, inMat.shape[1] - pad_x) if not zigZag or (y - pad_y) % 2 == 0 else (
                inMat.shape[1] - pad_x - 1, pad_x - 1, -1)):
            old_p = inMat[y, x]
            new_p = np.round(samplingF * old_p / 255.0) * (255 / samplingF)
            inMat[y, x] = new_p
            quant_error_p = old_p - new_p

            inMat[y, x + 1] = minmax(inMat[y, x + 1] + quant_error_p * 8 / 32.0)
            inMat[y, x + 2] = minmax(inMat[y, x + 2] + quant_error_p * 4 / 32.0)
            inMat[y + 1, x - 2] = minmax(inMat[y + 1, x - 2] + quant_error_p * 2 / 32.0)
            inMat[y + 1, x - 1] = minmax(inMat[y + 1, x - 1] + quant_error_p * 4 / 32.0)
            inMat[y + 1, x] = minmax(inMat[y + 1, x] + quant_error_p * 8 / 32.0)
            inMat[y + 1, x + 1] = minmax(inMat[y + 1, x + 1] + quant_error_p * 4 / 32.0)
            inMat[y + 1, x + 2] = minmax(inMat[y + 1, x + 2] + quant_error_p * 2 / 32.0)

    return inMat[pad_y:inMat.shape[0] - pad_y, pad_x:inMat.shape[1] - pad_x]


def burkes_color(inMat, zigZag=False, samplingF=1):
    pad_y = 1
    pad_x = 2
    inMat = cv2.copyMakeBorder(inMat, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)

    for y in range(pad_y, inMat.shape[0] - pad_y):
        for x in range(*(pad_x, inMat.shape[1] - pad_x) if not zigZag or (y - pad_y) % 2 == 0 else (
                inMat.shape[1] - pad_x - 1, pad_x - 1, -1)):
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

            inMat[y, x + 1, 0] = minmax(inMat[y, x + 1, 0] + quant_error_b * 8 / 32.0)
            inMat[y, x + 1, 1] = minmax(inMat[y, x + 1, 1] + quant_error_g * 8 / 32.0)
            inMat[y, x + 1, 2] = minmax(inMat[y, x + 1, 2] + quant_error_r * 8 / 32.0)

            inMat[y, x + 2, 0] = minmax(inMat[y, x + 2, 0] + quant_error_b * 4 / 32.0)
            inMat[y, x + 2, 1] = minmax(inMat[y, x + 2, 1] + quant_error_g * 4 / 32.0)
            inMat[y, x + 2, 2] = minmax(inMat[y, x + 2, 2] + quant_error_r * 4 / 32.0)

            inMat[y + 1, x - 2, 0] = minmax(inMat[y + 1, x - 2, 0] + quant_error_b * 2 / 32.0)
            inMat[y + 1, x - 2, 1] = minmax(inMat[y + 1, x - 2, 1] + quant_error_g * 2 / 32.0)
            inMat[y + 1, x - 2, 2] = minmax(inMat[y + 1, x - 2, 2] + quant_error_r * 2 / 32.0)

            inMat[y + 1, x - 1, 0] = minmax(inMat[y + 1, x - 1, 0] + quant_error_b * 4 / 32.0)
            inMat[y + 1, x - 1, 1] = minmax(inMat[y + 1, x - 1, 1] + quant_error_g * 4 / 32.0)
            inMat[y + 1, x - 1, 2] = minmax(inMat[y + 1, x - 1, 2] + quant_error_r * 4 / 32.0)

            inMat[y + 1, x, 0] = minmax(inMat[y + 1, x, 0] + quant_error_b * 8 / 32.0)
            inMat[y + 1, x, 1] = minmax(inMat[y + 1, x, 1] + quant_error_g * 8 / 32.0)
            inMat[y + 1, x, 2] = minmax(inMat[y + 1, x, 2] + quant_error_r * 8 / 32.0)

            inMat[y + 1, x + 1, 0] = minmax(inMat[y + 1, x + 1, 0] + quant_error_b * 4 / 32.0)
            inMat[y + 1, x + 1, 1] = minmax(inMat[y + 1, x + 1, 1] + quant_error_g * 4 / 32.0)
            inMat[y + 1, x + 1, 2] = minmax(inMat[y + 1, x + 1, 2] + quant_error_r * 4 / 32.0)

            inMat[y + 1, x + 2, 0] = minmax(inMat[y + 1, x + 2, 0] + quant_error_b * 2 / 32.0)
            inMat[y + 1, x + 2, 1] = minmax(inMat[y + 1, x + 2, 1] + quant_error_g * 2 / 32.0)
            inMat[y + 1, x + 2, 2] = minmax(inMat[y + 1, x + 2, 2] + quant_error_r * 2 / 32.0)

    return inMat[pad_y:inMat.shape[0] - pad_y, pad_x:inMat.shape[1] - pad_x]


def sierra_gray(inMat, zigZag=True, samplingF=1):
    pad_y = pad_x = 2
    inMat = cv2.copyMakeBorder(inMat, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)

    for y in range(pad_y, inMat.shape[0] - pad_y):
        for x in range(*(pad_x, inMat.shape[1] - pad_x) if not zigZag or (y - pad_y) % 2 == 0 else (
                inMat.shape[1] - pad_x - 1, pad_x - 1, -1)):
            old_p = inMat[y, x]
            new_p = np.round(samplingF * old_p / 255.0) * (255 / samplingF)
            inMat[y, x] = new_p
            quant_error_p = old_p - new_p

            inMat[y, x + 1] = minmax(inMat[y, x + 1] + quant_error_p * 5 / 32.0)
            inMat[y, x + 2] = minmax(inMat[y, x + 2] + quant_error_p * 3 / 32.0)

            inMat[y + 1, x - 2] = minmax(inMat[y + 1, x - 2] + quant_error_p * 2 / 32.0)
            inMat[y + 1, x - 1] = minmax(inMat[y + 1, x - 1] + quant_error_p * 4 / 32.0)
            inMat[y + 1, x] = minmax(inMat[y + 1, x] + quant_error_p * 5 / 32.0)
            inMat[y + 1, x + 1] = minmax(inMat[y + 1, x + 1] + quant_error_p * 4 / 32.0)
            inMat[y + 1, x + 2] = minmax(inMat[y + 1, x + 2] + quant_error_p * 2 / 32.0)

            inMat[y + 2, x - 1] = minmax(inMat[y + 2, x - 1] + quant_error_p * 2 / 32.0)
            inMat[y + 2, x] = minmax(inMat[y + 2, x] + quant_error_p * 3 / 32.0)
            inMat[y + 2, x + 1] = minmax(inMat[y + 2, x + 1] + quant_error_p * 2 / 32.0)

    return inMat[pad_y:inMat.shape[0] - pad_y, pad_x:inMat.shape[1] - pad_x]


def sierra_color(inMat, zigZag=False, samplingF=1):
    pad_y = pad_x = 2
    inMat = cv2.copyMakeBorder(inMat, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)

    for y in range(pad_y, inMat.shape[0] - pad_y):
        for x in range(*(pad_x, inMat.shape[1] - pad_x) if not zigZag or (y - pad_y) % 2 == 0 else (
                inMat.shape[1] - pad_x - 1, pad_x - 1, -1)):
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

            inMat[y, x + 1, 0] = minmax(inMat[y, x + 1, 0] + quant_error_b * 5 / 32.0)
            inMat[y, x + 1, 1] = minmax(inMat[y, x + 1, 1] + quant_error_g * 5 / 32.0)
            inMat[y, x + 1, 2] = minmax(inMat[y, x + 1, 2] + quant_error_r * 5 / 32.0)

            inMat[y, x + 2, 0] = minmax(inMat[y, x + 2, 0] + quant_error_b * 3 / 32.0)
            inMat[y, x + 2, 1] = minmax(inMat[y, x + 2, 1] + quant_error_g * 3 / 32.0)
            inMat[y, x + 2, 2] = minmax(inMat[y, x + 2, 2] + quant_error_r * 3 / 32.0)

            inMat[y + 1, x - 2, 0] = minmax(inMat[y + 1, x - 2, 0] + quant_error_b * 2 / 32.0)
            inMat[y + 1, x - 2, 1] = minmax(inMat[y + 1, x - 2, 1] + quant_error_g * 2 / 32.0)
            inMat[y + 1, x - 2, 2] = minmax(inMat[y + 1, x - 2, 2] + quant_error_r * 2 / 32.0)

            inMat[y + 1, x - 1, 0] = minmax(inMat[y + 1, x - 1, 0] + quant_error_b * 4 / 32.0)
            inMat[y + 1, x - 1, 1] = minmax(inMat[y + 1, x - 1, 1] + quant_error_g * 4 / 32.0)
            inMat[y + 1, x - 1, 2] = minmax(inMat[y + 1, x - 1, 2] + quant_error_r * 4 / 32.0)

            inMat[y + 1, x, 0] = minmax(inMat[y + 1, x, 0] + quant_error_b * 5 / 32.0)
            inMat[y + 1, x, 1] = minmax(inMat[y + 1, x, 1] + quant_error_g * 5 / 32.0)
            inMat[y + 1, x, 2] = minmax(inMat[y + 1, x, 2] + quant_error_r * 5 / 32.0)

            inMat[y + 1, x + 1, 0] = minmax(inMat[y + 1, x + 1, 0] + quant_error_b * 4 / 32.0)
            inMat[y + 1, x + 1, 1] = minmax(inMat[y + 1, x + 1, 1] + quant_error_g * 4 / 32.0)
            inMat[y + 1, x + 1, 2] = minmax(inMat[y + 1, x + 1, 2] + quant_error_r * 4 / 32.0)

            inMat[y + 1, x + 2, 0] = minmax(inMat[y + 1, x + 2, 0] + quant_error_b * 2 / 32.0)
            inMat[y + 1, x + 2, 1] = minmax(inMat[y + 1, x + 2, 1] + quant_error_g * 2 / 32.0)
            inMat[y + 1, x + 2, 2] = minmax(inMat[y + 1, x + 2, 2] + quant_error_r * 2 / 32.0)

            inMat[y + 2, x - 1, 0] = minmax(inMat[y + 2, x - 1, 0] + quant_error_b * 2 / 32.0)
            inMat[y + 2, x - 1, 1] = minmax(inMat[y + 2, x - 1, 1] + quant_error_g * 2 / 32.0)
            inMat[y + 2, x - 1, 2] = minmax(inMat[y + 2, x - 1, 2] + quant_error_r * 2 / 32.0)

            inMat[y + 2, x, 0] = minmax(inMat[y + 2, x, 0] + quant_error_b * 3 / 32.0)
            inMat[y + 2, x, 1] = minmax(inMat[y + 2, x, 1] + quant_error_g * 3 / 32.0)
            inMat[y + 2, x, 2] = minmax(inMat[y + 2, x, 2] + quant_error_r * 3 / 32.0)

            inMat[y + 2, x + 1, 0] = minmax(inMat[y + 2, x + 1, 0] + quant_error_b * 2 / 32.0)
            inMat[y + 2, x + 1, 1] = minmax(inMat[y + 2, x + 1, 1] + quant_error_g * 2 / 32.0)
            inMat[y + 2, x + 1, 2] = minmax(inMat[y + 2, x + 1, 2] + quant_error_r * 2 / 32.0)

    return inMat[pad_y:inMat.shape[0] - pad_y, pad_x:inMat.shape[1] - pad_x]


def stucki_gray(inMat, zigZag=True, samplingF=1):
    pad_y = pad_x = 2
    inMat = cv2.copyMakeBorder(inMat, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)

    for y in range(pad_y, inMat.shape[0] - pad_y):
        for x in range(*(pad_x, inMat.shape[1] - pad_x) if not zigZag or (y - pad_y) % 2 == 0 else (
                inMat.shape[1] - pad_x - 1, pad_x - 1, -1)):
            old_p = inMat[y, x]
            new_p = np.round(samplingF * old_p / 255.0) * (255 / samplingF)
            inMat[y, x] = new_p
            quant_error_p = old_p - new_p

            inMat[y, x + 1] = minmax(inMat[y, x + 1] + quant_error_p * 8 / 42.0)
            inMat[y, x + 2] = minmax(inMat[y, x + 2] + quant_error_p * 4 / 42.0)

            inMat[y + 1, x - 2] = minmax(inMat[y + 1, x - 2] + quant_error_p * 2 / 42.0)
            inMat[y + 1, x - 1] = minmax(inMat[y + 1, x - 1] + quant_error_p * 4 / 42.0)
            inMat[y + 1, x] = minmax(inMat[y + 1, x] + quant_error_p * 8 / 42.0)
            inMat[y + 1, x + 1] = minmax(inMat[y + 1, x + 1] + quant_error_p * 4 / 42.0)
            inMat[y + 1, x + 2] = minmax(inMat[y + 1, x + 2] + quant_error_p * 2 / 42.0)

            inMat[y + 1, x - 2] = minmax(inMat[y + 1, x - 2] + quant_error_p * 1 / 42.0)
            inMat[y + 1, x - 1] = minmax(inMat[y + 1, x - 1] + quant_error_p * 2 / 42.0)
            inMat[y + 1, x] = minmax(inMat[y + 1, x] + quant_error_p * 4 / 42.0)
            inMat[y + 1, x + 1] = minmax(inMat[y + 1, x + 1] + quant_error_p * 2 / 42.0)
            inMat[y + 1, x + 2] = minmax(inMat[y + 1, x + 2] + quant_error_p * 1 / 42.0)

    return inMat[pad_y:inMat.shape[0] - pad_y, pad_x:inMat.shape[1] - pad_x]


def stucki_color(inMat, zigZag=False, samplingF=1):
    pad_y = pad_x = 2
    inMat = cv2.copyMakeBorder(inMat, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)

    for y in range(pad_y, inMat.shape[0] - pad_y):
        for x in range(*(pad_x, inMat.shape[1] - pad_x) if not zigZag or (y - pad_y) % 2 == 0 else (
                inMat.shape[1] - pad_x - 1, pad_x - 1, -1)):
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

            inMat[y, x + 1, 0] = minmax(inMat[y, x + 1, 0] + quant_error_b * 8 / 42.0)
            inMat[y, x + 1, 1] = minmax(inMat[y, x + 1, 1] + quant_error_g * 8 / 42.0)
            inMat[y, x + 1, 2] = minmax(inMat[y, x + 1, 2] + quant_error_r * 8 / 42.0)

            inMat[y, x + 2, 0] = minmax(inMat[y, x + 2, 0] + quant_error_b * 4 / 42.0)
            inMat[y, x + 2, 1] = minmax(inMat[y, x + 2, 1] + quant_error_g * 4 / 42.0)
            inMat[y, x + 2, 2] = minmax(inMat[y, x + 2, 2] + quant_error_r * 4 / 42.0)

            inMat[y + 1, x - 2, 0] = minmax(inMat[y + 1, x - 2, 0] + quant_error_b * 2 / 42.0)
            inMat[y + 1, x - 2, 1] = minmax(inMat[y + 1, x - 2, 1] + quant_error_g * 2 / 42.0)
            inMat[y + 1, x - 2, 2] = minmax(inMat[y + 1, x - 2, 2] + quant_error_r * 2 / 42.0)

            inMat[y + 1, x - 1, 0] = minmax(inMat[y + 1, x - 1, 0] + quant_error_b * 4 / 42.0)
            inMat[y + 1, x - 1, 1] = minmax(inMat[y + 1, x - 1, 1] + quant_error_g * 4 / 42.0)
            inMat[y + 1, x - 1, 2] = minmax(inMat[y + 1, x - 1, 2] + quant_error_r * 4 / 42.0)

            inMat[y + 1, x, 0] = minmax(inMat[y + 1, x, 0] + quant_error_b * 8 / 42.0)
            inMat[y + 1, x, 1] = minmax(inMat[y + 1, x, 1] + quant_error_g * 8 / 42.0)
            inMat[y + 1, x, 2] = minmax(inMat[y + 1, x, 2] + quant_error_r * 8 / 42.0)

            inMat[y + 1, x + 1, 0] = minmax(inMat[y + 1, x + 1, 0] + quant_error_b * 4 / 42.0)
            inMat[y + 1, x + 1, 1] = minmax(inMat[y + 1, x + 1, 1] + quant_error_g * 4 / 42.0)
            inMat[y + 1, x + 1, 2] = minmax(inMat[y + 1, x + 1, 2] + quant_error_r * 4 / 42.0)

            inMat[y + 1, x + 2, 0] = minmax(inMat[y + 1, x + 2, 0] + quant_error_b * 2 / 42.0)
            inMat[y + 1, x + 2, 1] = minmax(inMat[y + 1, x + 2, 1] + quant_error_g * 2 / 42.0)
            inMat[y + 1, x + 2, 2] = minmax(inMat[y + 1, x + 2, 2] + quant_error_r * 2 / 42.0)

            inMat[y + 1, x - 2, 0] = minmax(inMat[y + 1, x - 2, 0] + quant_error_b * 1 / 42.0)
            inMat[y + 1, x - 2, 1] = minmax(inMat[y + 1, x - 2, 1] + quant_error_g * 1 / 42.0)
            inMat[y + 1, x - 2, 2] = minmax(inMat[y + 1, x - 2, 2] + quant_error_r * 1 / 42.0)

            inMat[y + 1, x - 1, 0] = minmax(inMat[y + 1, x - 1, 0] + quant_error_b * 2 / 42.0)
            inMat[y + 1, x - 1, 1] = minmax(inMat[y + 1, x - 1, 1] + quant_error_g * 2 / 42.0)
            inMat[y + 1, x - 1, 2] = minmax(inMat[y + 1, x - 1, 2] + quant_error_r * 2 / 42.0)

            inMat[y + 1, x, 0] = minmax(inMat[y + 1, x, 0] + quant_error_b * 4 / 42.0)
            inMat[y + 1, x, 1] = minmax(inMat[y + 1, x, 1] + quant_error_g * 4 / 42.0)
            inMat[y + 1, x, 2] = minmax(inMat[y + 1, x, 2] + quant_error_r * 4 / 42.0)

            inMat[y + 1, x + 1, 0] = minmax(inMat[y + 1, x + 1, 0] + quant_error_b * 2 / 42.0)
            inMat[y + 1, x + 1, 1] = minmax(inMat[y + 1, x + 1, 1] + quant_error_g * 2 / 42.0)
            inMat[y + 1, x + 1, 2] = minmax(inMat[y + 1, x + 1, 2] + quant_error_r * 2 / 42.0)

            inMat[y + 1, x + 2, 0] = minmax(inMat[y + 1, x + 2, 0] + quant_error_b * 1 / 42.0)
            inMat[y + 1, x + 2, 1] = minmax(inMat[y + 1, x + 2, 1] + quant_error_g * 1 / 42.0)
            inMat[y + 1, x + 2, 2] = minmax(inMat[y + 1, x + 2, 2] + quant_error_r * 1 / 42.0)

    return inMat[pad_y:inMat.shape[0] - pad_y, pad_x:inMat.shape[1] - pad_x]


def jarvis_judice_ninke_gray(inMat, zigZag=True, samplingF=1):
    pad_y = pad_x = 2
    inMat = cv2.copyMakeBorder(inMat, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)

    for y in range(pad_y, inMat.shape[0] - pad_y):
        for x in range(*(pad_x, inMat.shape[1] - pad_x) if not zigZag or (y - pad_y) % 2 == 0 else (
                inMat.shape[1] - pad_x - 1, pad_x - 1, -1)):
            old_p = inMat[y, x]
            new_p = np.round(samplingF * old_p / 255.0) * (255 / samplingF)
            inMat[y, x] = new_p
            quant_error_p = old_p - new_p

            inMat[y, x + 1] = minmax(inMat[y, x + 1] + quant_error_p * 7 / 48.0)
            inMat[y, x + 2] = minmax(inMat[y, x + 2] + quant_error_p * 5 / 48.0)

            inMat[y + 1, x - 2] = minmax(inMat[y + 1, x - 2] + quant_error_p * 3 / 48.0)
            inMat[y + 1, x - 1] = minmax(inMat[y + 1, x - 1] + quant_error_p * 5 / 48.0)
            inMat[y + 1, x] = minmax(inMat[y + 1, x] + quant_error_p * 7 / 42.0)
            inMat[y + 1, x + 1] = minmax(inMat[y + 1, x + 1] + quant_error_p * 5 / 48.0)
            inMat[y + 1, x + 2] = minmax(inMat[y + 1, x + 2] + quant_error_p * 3 / 48.0)

            inMat[y + 1, x - 2] = minmax(inMat[y + 1, x - 2] + quant_error_p * 1 / 48.0)
            inMat[y + 1, x - 1] = minmax(inMat[y + 1, x - 1] + quant_error_p * 3 / 48.0)
            inMat[y + 1, x] = minmax(inMat[y + 1, x] + quant_error_p * 5 / 48.0)
            inMat[y + 1, x + 1] = minmax(inMat[y + 1, x + 1] + quant_error_p * 3 / 48.0)
            inMat[y + 1, x + 2] = minmax(inMat[y + 1, x + 2] + quant_error_p * 1 / 48.0)

    return inMat[pad_y:inMat.shape[0] - pad_y, pad_x:inMat.shape[1] - pad_x]


def jarvis_judice_ninke_color(inMat, zigZag=False, samplingF=1):
    pad_y = pad_x = 2
    inMat = cv2.copyMakeBorder(inMat, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)

    for y in range(pad_y, inMat.shape[0] - pad_y):
        for x in range(*(pad_x, inMat.shape[1] - pad_x) if not zigZag or (y - pad_y) % 2 == 0 else (
                inMat.shape[1] - pad_x - 1, pad_x - 1, -1)):
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

            inMat[y, x + 1, 0] = minmax(inMat[y, x + 1, 0] + quant_error_b * 7 / 48.0)
            inMat[y, x + 1, 1] = minmax(inMat[y, x + 1, 1] + quant_error_g * 7 / 48.0)
            inMat[y, x + 1, 2] = minmax(inMat[y, x + 1, 2] + quant_error_r * 7 / 48.0)

            inMat[y, x + 2, 0] = minmax(inMat[y, x + 2, 0] + quant_error_b * 5 / 48.0)
            inMat[y, x + 2, 1] = minmax(inMat[y, x + 2, 1] + quant_error_g * 5 / 48.0)
            inMat[y, x + 2, 2] = minmax(inMat[y, x + 2, 2] + quant_error_r * 5 / 48.0)

            inMat[y + 1, x - 2, 0] = minmax(inMat[y + 1, x - 2, 0] + quant_error_b * 3 / 48.0)
            inMat[y + 1, x - 2, 1] = minmax(inMat[y + 1, x - 2, 1] + quant_error_g * 3 / 48.0)
            inMat[y + 1, x - 2, 2] = minmax(inMat[y + 1, x - 2, 2] + quant_error_r * 3 / 48.0)

            inMat[y + 1, x - 1, 0] = minmax(inMat[y + 1, x - 1, 0] + quant_error_b * 5 / 48.0)
            inMat[y + 1, x - 1, 1] = minmax(inMat[y + 1, x - 1, 1] + quant_error_g * 5 / 48.0)
            inMat[y + 1, x - 1, 2] = minmax(inMat[y + 1, x - 1, 2] + quant_error_r * 5 / 48.0)

            inMat[y + 1, x, 0] = minmax(inMat[y + 1, x, 0] + quant_error_b * 7 / 48.0)
            inMat[y + 1, x, 1] = minmax(inMat[y + 1, x, 1] + quant_error_g * 7 / 48.0)
            inMat[y + 1, x, 2] = minmax(inMat[y + 1, x, 2] + quant_error_r * 7 / 48.0)

            inMat[y + 1, x + 1, 0] = minmax(inMat[y + 1, x + 1, 0] + quant_error_b * 5 / 48.0)
            inMat[y + 1, x + 1, 1] = minmax(inMat[y + 1, x + 1, 1] + quant_error_g * 5 / 48.0)
            inMat[y + 1, x + 1, 2] = minmax(inMat[y + 1, x + 1, 2] + quant_error_r * 5 / 48.0)

            inMat[y + 1, x + 2, 0] = minmax(inMat[y + 1, x + 2, 0] + quant_error_b * 3 / 48.0)
            inMat[y + 1, x + 2, 1] = minmax(inMat[y + 1, x + 2, 1] + quant_error_g * 3 / 48.0)
            inMat[y + 1, x + 2, 2] = minmax(inMat[y + 1, x + 2, 2] + quant_error_r * 3 / 48.0)

            inMat[y + 1, x - 2, 0] = minmax(inMat[y + 1, x - 2, 0] + quant_error_b * 1 / 48.0)
            inMat[y + 1, x - 2, 1] = minmax(inMat[y + 1, x - 2, 1] + quant_error_g * 1 / 48.0)
            inMat[y + 1, x - 2, 2] = minmax(inMat[y + 1, x - 2, 2] + quant_error_r * 1 / 48.0)

            inMat[y + 1, x - 1, 0] = minmax(inMat[y + 1, x - 1, 0] + quant_error_b * 3 / 48.0)
            inMat[y + 1, x - 1, 1] = minmax(inMat[y + 1, x - 1, 1] + quant_error_g * 3 / 48.0)
            inMat[y + 1, x - 1, 2] = minmax(inMat[y + 1, x - 1, 2] + quant_error_r * 3 / 48.0)

            inMat[y + 1, x, 0] = minmax(inMat[y + 1, x, 0] + quant_error_b * 5 / 48.0)
            inMat[y + 1, x, 1] = minmax(inMat[y + 1, x, 1] + quant_error_g * 5 / 48.0)
            inMat[y + 1, x, 2] = minmax(inMat[y + 1, x, 2] + quant_error_r * 5 / 48.0)

            inMat[y + 1, x + 1, 0] = minmax(inMat[y + 1, x + 1, 0] + quant_error_b * 3 / 48.0)
            inMat[y + 1, x + 1, 1] = minmax(inMat[y + 1, x + 1, 1] + quant_error_g * 3 / 48.0)
            inMat[y + 1, x + 1, 2] = minmax(inMat[y + 1, x + 1, 2] + quant_error_r * 3 / 48.0)

            inMat[y + 1, x + 2, 0] = minmax(inMat[y + 1, x + 2, 0] + quant_error_b * 1 / 48.0)
            inMat[y + 1, x + 2, 1] = minmax(inMat[y + 1, x + 2, 1] + quant_error_g * 1 / 48.0)
            inMat[y + 1, x + 2, 2] = minmax(inMat[y + 1, x + 2, 2] + quant_error_r * 1 / 48.0)

    return inMat[pad_y:inMat.shape[0] - pad_y, pad_x:inMat.shape[1] - pad_x]


# # TODO: Implementar o padding
# def conventional_scan(img, algorithm):
#     for y in range(img.shape[0]):
#         for x in range(img.shape[1]):
#             algorithm(img, y, x)
#
#
# # TODO: Implementar o padding
# def alternate_scan(img, algorithm):
#     for y in range(img.shape[0]):
#         for x in range(*(0, img.shape[1], 1) if y % 2 == 0 else (img.shape[1] - 1, -1, -1)):
#             algorithm(img, y, x)
#
#
# def dithering(img, scan_mode, algorithm):
#     new_img = conventional_scan(img, algorithm) if scan_mode == 0 else alternate_scan(img, algorithm)
#     return new_img


algorithms = ((floyd_steinberg_gray, floyd_steinberg_color),
              (stevenson_arce_gray, stevenson_arce_color),
              (burkes_gray, burkes_color),
              (sierra_gray, sierra_color),
              (stucki_gray, stucki_color),
              (jarvis_judice_ninke_gray, jarvis_judice_ninke_color))


def main():
    # img = np.array([[100, 76, 15, 189], [201, 173, 28, 120], [127, 168, 69, 128]], dtype=np.uint8)

    alg = 1

    img = cv2.imread('./../in/baboon.png', 0)
    new_img = algorithms[alg][0](img, True)
    cv2.imwrite('./../out/baboon-gray-' + str(alg) + '.png', new_img)

    img = cv2.imread('./../in/baboon.png')
    new_img = algorithms[alg][1](img, True)
    cv2.imwrite('./../out/baboon-color-' + str(alg) + '.png', new_img)


if __name__ == "__main__":
    main()

# 26.812670946121216
# 8.961915016174316
# 42.00108814239502
# 13.64300274848938
