import argparse
import time
import cv2
import numpy as np


def run_task(desc, func, *args):
    print("Running:", desc)
    start = time.time()
    values = func(*args)
    end = time.time()
    print("Finishing", desc + ":", round((end - start) * 1000))
    return values


def parse_args():
    parser = argparse.ArgumentParser()

    in_group = parser.add_mutually_exclusive_group()
    in_group.add_argument('input', type=str, nargs='?', default='in', help="input-file or input-dir")
    in_group.add_argument('-i', '--in', '--input', type=str, nargs='+', dest='input_o', help='input-file or input-dir')

    out_group = parser.add_mutually_exclusive_group()
    out_group.add_argument('output', type=str, nargs='?', default='out', help="output-file or output-dir")
    out_group.add_argument('-o', '--out', '--output', type=str, nargs='+', dest='output_o',
                           help='output-file or output-dir')

    parser.add_argument('-c', '--color', type=int, nargs='+', choices=[0, 1], default=[1], help='image color mode')
    parser.add_argument('-a', '--alg', '--algorithm', type=int, nargs='+', choices=[0, 1, 2, 3, 4, 5], default=[0],
                        dest='alg', help='dithering algorithm')
    parser.add_argument('-d', '--direction', type=int, nargs='+', choices=[0, 1], default=[0], dest='dir',
                        help='scan direction')

    args = parser.parse_args()
    return [args.input] if args.input_o is None else args.input_o, \
           [args.output] if args.output_o is None else args.output_o, args.color, args.alg, args.dir


def scan_top_down(img, func):
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            func(img, y, x)


def scan_top_down_alternate(img, func):
    for y in range(img.shape[0]):
        for x in range(*(0, img.shape[1], 1) if y % 2 == 0 else (img.shape[1] - 1, -1, -1)):
            func(img, y, x)


def scan_top_down_next(m, x, y):
    return ++x


class Mask:
    def __init__(self, name, padding, values):
        self.name = name
        self.padding = padding
        self.values = values


_MASKS = (Mask("Floyd and Steinberg", (1, 1), ((0, 1, 0.4375), (1, -1, 0.1875), (1, 0, 0.3125), (1, 1, 0.0625))),

          Mask("Stevenson and Arce", (3, 3),
               ((0, 2, 0.16),
                (1, -3, 0.06), (1, -1, 0.13), (1, 1, 0.15), (1, 3, 0.08),
                (2, -2, 0.06), (2, 0, 0.13), (2, 2, 0.06),
                (3, -3, 0.025), (3, -1, 0.06), (3, 1, 0.06), (3, 3, 0.025))),

          Mask("Burkes", (1, 2),
               ((0, 1, 0.25), (0, 2, 0.125),
                (1, -2, 0.0625), (1, -1, 0.125), (1, 0, 0.25), (1, 1, 0.125), (1, 2, 0.0625))),

          Mask("Sierra", (2, 2),
               ((0, 1, 0.15625), (0, 2, 0.09375),
                (1, -2, 0.0625), (1, -1, 0.125), (1, 0, 0.15625), (1, 1, 0.125), (1, 2, 0.0625),
                (2, -1, 0.0625), (2, 0, 0.9375), (2, 1, 0.0625))),

          Mask("Stucki", (2, 2),
               ((0, 1, 0.19047619047), (0, 2, 0.09523809523),
                (1, -2, 0.04761904761), (1, -1, 0.09523809523), (1, 0, 0.19047619047), (1, 1, 0.09523809523),
                (1, 2, 0.04761904761),
                (2, -2, 0.02380952380), (2, -1, 0.04761904761), (2, 0, 0.09523809523), (2, 1, 0.04761904761),
                (2, 2, 0.02380952380))),

          Mask("Jarvis, Judice and Ninke", (2, 2),
               ((0, 1, 0.14583333333), (0, 2, 0.10416666666),
                (1, -2, 0.0625), (1, -1, 0.10416666666), (1, 0, 0.14583333333), (1, 1, 0.10416666666), (1, 2, 0.0625),
                (2, -2, 0.022083333333), (2, -1, 0.0625), (2, 0, 0.10416666666), (2, 1, 0.0625),
                (2, 2, 0.022083333333))))


def minmax(v):
    return 0 if v < 0 else 255 if v > 255 else v


def dithering(img, y, x, mask, samplingF=1.0):
    if len(img.shape) > 2:
        old_b = img[y, x, 0]
        old_g = img[y, x, 1]
        old_r = img[y, x, 2]
        new_b = np.round(samplingF * old_b / 255.0) * (255 / samplingF)
        new_g = np.round(samplingF * old_g / 255.0) * (255 / samplingF)
        new_r = np.round(samplingF * old_r / 255.0) * (255 / samplingF)
        error_b = old_b - new_b
        error_g = old_g - new_g
        error_r = old_r - new_r
        for m in mask.values:
            pos_y = y + m[0]
            pos_x = x + m[1]
            img[pos_y, pos_x, 0] = minmax(img[pos_y, pos_x, 0] + error_b * m[2])
            img[pos_y, pos_x, 1] = minmax(img[pos_y, pos_x, 1] + error_g * m[2])
            img[pos_y, pos_x, 2] = minmax(img[pos_y, pos_x, 2] + error_r * m[2])
    else:
        old_px = img[y, x]
        new_px = np.round(samplingF * old_px / 255.0) * (255 / samplingF)
        img[y, x] = new_px
        error = old_px - new_px
        for m in mask.values:
            pos_y = y + m[0]
            pos_x = x + m[1]
            img[pos_y, pos_x] = minmax(img[pos_y, pos_x] + error * m[2])


def faz_a_porcaria(img):
    pad_y = pad_x = 1
    img = cv2.copyMakeBorder(img, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)
    for y in range(pad_y, img.shape[0] - pad_y):
        for x in range(pad_x, img.shape[1] - pad_x):
            dithering(img, y, x, _MASKS[0], 2.5)
    return img[pad_y:img.shape[0] - pad_y, pad_x:img.shape[1] - pad_x]


def my_dithering_gray(inMat, samplingF=1.0):
    inicio = time.time()
    h = inMat.shape[0]
    w = inMat.shape[1]

    # print(inMat)

    for y in range(0, h - 1):
        for x in range(1, w - 1):
            dithering(inMat, y, x, _MASKS[0], 1)

    fim = time.time()
    print(fim - inicio)
    print(inMat)

    return inMat


def dithering_gray(inMat, samplingF=1.0):
    inicio = time.time()
    h = inMat.shape[0]
    w = inMat.shape[1]

    print(inMat)

    for y in range(0, h - 1):
        for x in range(1, w - 1):
            old_p = inMat[y, x]
            new_p = np.round(samplingF * old_p / 255.0) * (255 / samplingF)
            inMat[y, x] = new_p

            quant_error_p = old_p - new_p

            inMat[y, x + 1] = minmax(inMat[y, x + 1] + quant_error_p * 7 / 16.0)
            inMat[y + 1, x - 1] = minmax(inMat[y + 1, x - 1] + quant_error_p * 3 / 16.0)
            inMat[y + 1, x] = minmax(inMat[y + 1, x] + quant_error_p * 5 / 16.0)
            inMat[y + 1, x + 1] = minmax(inMat[y + 1, x + 1] + quant_error_p * 1 / 16.0)

    fim = time.time()
    print(fim - inicio)
    print(inMat)

    return inMat


def dithering_color(inMat, samplingF=1.0):
    inicio = time.time()

    h = inMat.shape[0]
    w = inMat.shape[1]

    for y in range(0, h - 1):
        for x in range(1, w - 1):
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

    fim = time.time()
    print(fim - inicio)

    return inMat


def main():
    inputs, outputs, colors, algorithms, scans = parse_args()
    img = np.array([[200, 30, 64, 100], [110, 127, 128, 138], [175, 200, 230, 55]], dtype=np.uint8)

    # img = cv2.imread('./../in/baboon.png', 0)
    # res = run_task("faz a porcaria", faz_a_porcaria, img)
    # cv2.imwrite('./../out/baboon-gray.png', res)

    # img = cv2.imread('./../in/baboon.png', 0)
    res = dithering_gray(img)
    print()
    # cv2.imwrite('./../out/baboon-gray-orig.png', res)
    #
    # img = cv2.imread('./../in/baboon.png')
    # res = dithering_color(img)
    # cv2.imwrite('./../out/baboon-color-orig.png', res)

    img = np.array([[200, 30, 64, 100], [110, 127, 128, 138], [175, 200, 230, 55]], dtype=np.uint8)
    my_dithering_gray(img)


if __name__ == "__main__":
    main()
