import argparse
import time
import cv2
import numpy as np


class Mask:
    def __init__(self, name, values):
        self.name = name
        self.values = values


__MASKS = (Mask('Floyd and Steinberg', ((0, 1, 0.4375), (1, -1, 0.1875), (1, 0, 0.3125), (1, 1, 0.0625))),

           Mask('Stevenson and Arce',
                ((0, 2, 0.16),
                 (1, -3, 0.06), (1, -1, 0.13), (1, 1, 0.15), (1, 3, 0.08),
                 (2, -2, 0.06), (2, 0, 0.13), (2, 2, 0.06),
                 (3, -3, 0.025), (3, -1, 0.06), (3, 1, 0.06), (3, 3, 0.025))),

           Mask('Burkes',
                ((0, 1, 0.25), (0, 2, 0.125),
                 (1, -2, 0.0625), (1, -1, 0.125), (1, 0, 0.25), (1, 1, 0.125), (1, 2, 0.0625))),

           Mask('Sierra',
                ((0, 1, 0.15625), (0, 2, 0.09375),
                 (1, -2, 0.0625), (1, -1, 0.125), (1, 0, 0.15625), (1, 1, 0.125), (1, 2, 0.0625),
                 (2, -1, 0.0625), (2, 0, 0.9375), (2, 1, 0.0625))),

           Mask('Stucki',
                ((0, 1, 0.19047619047), (0, 2, 0.09523809523),
                 (1, -2, 0.04761904761), (1, -1, 0.09523809523), (1, 0, 0.19047619047), (1, 1, 0.09523809523),
                 (1, 2, 0.04761904761),
                 (2, -2, 0.02380952380), (2, -1, 0.04761904761), (2, 0, 0.09523809523), (2, 1, 0.04761904761),
                 (2, 2, 0.02380952380))),

           Mask('Jarvis, Judice and Ninke',
                ((0, 1, 0.14583333333), (0, 2, 0.10416666666),
                 (1, -2, 0.0625), (1, -1, 0.10416666666), (1, 0, 0.14583333333), (1, 1, 0.10416666666), (1, 2, 0.0625),
                 (2, -2, 0.022083333333), (2, -1, 0.0625), (2, 0, 0.10416666666), (2, 1, 0.0625),
                 (2, 2, 0.022083333333))))


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
    parser.add_argument('-m', '--mask', type=int, nargs='+', choices=[0, 1, 2, 3, 4, 5], default=[0],
                        help='dithering algorithm')
    parser.add_argument('-d', '--direction', type=int, nargs='+', choices=[0, 1], default=[0], dest='dir',
                        help='scan direction')

    args = parser.parse_args()
    return [args.input] if args.input_o is None else args.input_o, \
           [args.output] if args.output_o is None else args.output_o, args.color, args.mask, args.dir


def minmax(v): return 0 if v < 0 else 255 if v > 255 else v


def dithering_gray(img, y, x, mask, sampling=1.0):
    old_px = img[y, x]
    new_px = np.round(sampling * old_px / 255.0) * (255 / sampling)
    img[y, x] = new_px
    error = old_px - new_px

    for m in mask:
        pos_y = y + m[0]
        pos_x = x + m[1]
        img[pos_y, pos_x] = minmax(img[pos_y, pos_x] + error * m[2])


def dithering_color(img, y, x, mask, sampling=1.0):
    old_b = img[y, x, 0]
    old_g = img[y, x, 1]
    old_r = img[y, x, 2]

    new_b = np.round(sampling * old_b / 255.0) * (255 / sampling)
    new_g = np.round(sampling * old_g / 255.0) * (255 / sampling)
    new_r = np.round(sampling * old_r / 255.0) * (255 / sampling)

    img[y, x, 0] = new_b
    img[y, x, 1] = new_g
    img[y, x, 2] = new_r

    error_b = old_b - new_b
    error_g = old_g - new_g
    error_r = old_r - new_r

    for m in mask:
        pos_y = y + m[0]
        pos_x = x + m[1]
        img[pos_y, pos_x, 0] = minmax(img[pos_y, pos_x, 0] + error_b * m[2])
        img[pos_y, pos_x, 1] = minmax(img[pos_y, pos_x, 1] + error_g * m[2])
        img[pos_y, pos_x, 2] = minmax(img[pos_y, pos_x, 2] + error_r * m[2])


def scan_top_down(img, func, *args, part=None):
    for y in range(part[0], part[1]):
        for x in range(part[2], part[3]):
            func(img, y, x, *args)


def mirror_mask(mask):
    ret = []
    for e in np.multiply(mask, (1, -1, 1)):
        ret.append((int(e[0]), int(e[1]), e[2]))
    return tuple(map(tuple, ret))


def scan_top_down_alt(img, func, *args, part=None):
    masks = (args[0], mirror_mask(args[0]))
    sampling = args[1]
    for y in range(part[0], part[1]):
        for x in range(*(part[2], part[3], 1) if y % 2 == 0 else (part[3] - 1, part[2] - 1, -1)):
            func(img, y, x, masks[y % 2], sampling)


__SCAN_FUNCTIONS = (scan_top_down, scan_top_down_alt)
__DITHERING_FUNCTIONS = (dithering_gray, dithering_color)


def dithering(img, color, mask, direction, sampling=1.0):
    pad_y, pad_x, _ = tuple(map(int, (np.max(np.abs(__MASKS[mask].values), axis=0))))
    img = cv2.copyMakeBorder(img, 0, pad_y, pad_x, pad_x, cv2.BORDER_REFLECT)

    scan_func = __SCAN_FUNCTIONS[direction]
    dithering_func = __DITHERING_FUNCTIONS[color]

    scan_func(img, dithering_func, __MASKS[mask].values, sampling,
              part=(0, img.shape[0] - pad_y, pad_x, img.shape[1] - pad_x))

    return img[0:img.shape[0] - pad_y, pad_x:img.shape[1] - pad_x]


def main():
    inputs, outputs, colors, masks, directions = parse_args()
    if len(inputs) != len(outputs):
        raise Exception("number of --input and --output parameters does not match")

    for i in range(len(inputs)):
        for color in colors:
            for mask in masks:
                for direction in directions:
                    img = cv2.imread(inputs[i], color)
                    img = run_task('dithering...', dithering, img, color, mask, direction)
                    cv2.imwrite(outputs[i], img)


if __name__ == "__main__":
    main()
