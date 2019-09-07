import numpy as np
import cv2
from itertools import chain


def floyd_steinberg(original, thresh=127, zig_zag=False):
    img = original
    cycle = 1
    c = 1
    if zig_zag:
        cycle = -1

    for y in range(img.shape[0] - 1):
        for x in chain(range(0, img.shape[1] - 1, 1),
                       range(img.shape[1] - 2, -1, cycle)):  # Controla o zig zague ou linear
            if (img[y][x] > thresh):
                dithering = 255
                err = img[y][x] - 255
            else:
                dithering = 0
                err = img[y][x] - 0

            img[y][x] = dithering

            img[y][x + c] = img[y][x + c] + err * (7 / 16)
            img[y + c][x - c] = img[y + c][x - c] + err * (3 / 16)
            img[y + c][x] = img[y + c][x] + err * (5 / 16)
            img[y + c][x + c] = img[y + c][x + c] + err * (1 / 16)
        c *= cycle  # Inverte a direção caso zig zague

    return img


img = cv2.imread('./../in/baboon.png', 0)  # 0 determina que a img é lida em tons de cinza
img1 = floyd_steinberg(img, zig_zag=True)  # percorrendo em zig zag
img2 = floyd_steinberg(img, zig_zag=False)  # percorrendo da esquerda para a direita

cv2.imshow('barcelona', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()