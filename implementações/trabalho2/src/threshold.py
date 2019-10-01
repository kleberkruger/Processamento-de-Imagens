import argparse
import os
import glob
import cv2
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt


def parse_args():
    parser = argparse.ArgumentParser()

    in_group = parser.add_mutually_exclusive_group()
    in_group.add_argument('input', type=str, nargs='?', default='in', help="input-file or input-dir")
    in_group.add_argument('-i', '--in', '--input', type=str, nargs='+', dest='input_o', help='input-file or input-dir')

    out_group = parser.add_mutually_exclusive_group()
    out_group.add_argument('output', type=str, nargs='?', default='out', help="output-file or output-dir")
    out_group.add_argument('-o', '--out', '--output', type=str, nargs='+', dest='output_o',
                           help='output-file or output-dir')

    parser.add_argument('-t', '--type', type=str, nargs='+', default='*',
                        help='image extension to scan within a directory')

    parser.add_argument('-g', '--global', type=int, nargs='*', dest='glob', help='global threshold value')
    parser.add_argument('-m', '--method', type=int, nargs='*', choices=[0, 1, 2, 3, 4, 5, 6], help='threshold method')
    parser.add_argument('-a', '--inv', '--invert', type=int, nargs='*', choices=[0, 1], dest='invert',
                        help='invert color mode')

    return parser.parse_args()


def get_arg_output(inputs, outputs):
    if outputs is not None:
        if len(outputs) != 1 and len(outputs) != len(inputs):
            raise Exception("number of <input> is not correspond to <output>")
        return outputs  # TODO: verificar regra 7?

    if inputs is None:
        return 'out'

    out_list = []
    for i in inputs:
        out_list.append(i if os.path.isdir(i) else str(Path(i).parent))
    return out_list


def get_output_file_name(orig, out):
    return out + '/' + orig if os.path.isdir(out) else out


def get_output_file_fullname(name, local, value):
    return os.path.splitext(name)[0] + ('-l' if local else '-g') + str(value) + '.pbm'


def get_images_in_directory(dir_path, extensions='*'):
    all_ext = ('*.bitmap', '*.gif', '*.jpeg', '*.pbm', '*.pgm', '*.png', '*.pnm', '*.ppm', '*.raw', '*.tiff', '*.svg')
    if extensions == '*':
        extensions = all_ext
    files = []
    for ext in extensions:
        files += [f for f in glob.glob(dir_path + "**/" + ext, recursive=False)]
    return files


def map_in_out(inputs, outputs, types):
    if len(outputs) < len(inputs):
        outputs = [outputs[0]] * len(inputs)

    files_map = []
    invalid_entries = []

    for i in range(len(inputs)):
        inp = str(Path(inputs[i]))
        if not os.path.exists(inp):
            invalid_entries.append(inp)
        elif not os.path.isdir(inp):
            files_map.append((inp, get_output_file_name(Path(inp).name, outputs[i])))
        # elif not os.path.isdir(outputs[i]):  # FIXME: se a pasta não existe, deixe para criar
        #     raise Exception("<output> is not a directory")
        else:
            for f in get_images_in_directory(inp, types):
                files_map.append((f, str(Path(outputs[i])) + '/' + Path(f).name))

    return files_map, invalid_entries


def get_arg_globs_methods(args):
    if args.glob is None and args.method is None:
        return [], [0]
    globs = [] if args.glob is None else [128] if not args.glob else args.glob
    methods = [] if args.method is None else [0] if not args.method else args.method
    return globs, methods


def get_args(args):
    inputs = [args.input] if args.input_o is None else args.input_o
    outputs = get_arg_output(inputs, args.output_o)
    globs, methods = get_arg_globs_methods(args)
    return inputs, outputs, args.type, globs, methods


__PX_OBJECT = (np.uint8(0), np.uint8(255))
__PX_BACKGROUND = (np.uint8(255), np.uint8(0))


def threshold_global(img, thresh=128):
    return np.where(img <= thresh, __PX_OBJECT, __PX_BACKGROUND)


def bernsen(mask, px, inv=False):
    z_min, z_max = np.min(mask), np.max(mask)
    t = (z_min + z_max) / 2
    return __PX_OBJECT[inv] if px > t else __PX_BACKGROUND[inv]
    # return (z_min + z_max) / 2


def niblack(mask, px, inv=False):
    k, mean, std = 0.2, np.mean(mask), np.std(mask)
    t = mean + k * std
    return __PX_OBJECT[inv] if px > t else __PX_BACKGROUND[inv]


def sauvola_pietaksinen(mask, px, inv=False):
    mean, std = np.mean(mask), np.std(mask)
    k, r = 0.5, 128
    t = mean * (1 + k * ((std / r) - 1))
    return __PX_OBJECT[inv] if px > t else __PX_BACKGROUND[inv]


def phansalskar_more_sabale(mask, px, inv=False):
    k, r, p, q = 0.25, 0.5, 2, 10
    mean, std = np.mean(mask), np.std(mask)
    t = mean * (1 + p * np.exp(-q * mean) + k * (std / r - 1))
    return __PX_OBJECT[inv] if px > t else __PX_BACKGROUND[inv]


def contrast(mask, px, inv=False):
    z_min, z_max = np.min(mask), np.max(mask)
    return __PX_OBJECT[inv] if abs(px - z_min) < abs(px - z_max) else __PX_BACKGROUND[inv]


def mean(mask, px, inv=False):
    t = np.mean(mask)
    return __PX_OBJECT[inv] if px > t else __PX_BACKGROUND[inv]


def median(mask, px, inv=False):
    t = np.median(mask)
    return __PX_OBJECT[inv] if px > t else __PX_BACKGROUND[inv]


__METHODS = [(bernsen, 1), (niblack, 1), (sauvola_pietaksinen, 1), (phansalskar_more_sabale, 1),
             (contrast, 1), (mean, 1), (median, 1)]


def threshold_local(img, method=0):
    func, m = __METHODS[method]
    res = np.zeros(img.shape, dtype=np.uint8)

    img = cv2.copyMakeBorder(img, m, m, m, m, cv2.BORDER_REFLECT)
    for y in range(m, img.shape[0] - m):
        for x in range(m, img.shape[1] - m):
            mask = img[y - m:y + m + 1, x - m:x + m + 1]
            # res[y - m][x - m] = __MIN_VALUE if img[y][x] <= func(mask) else __MAX_VALUE
            res[y - m][x - m] = func(mask, img[y][x])
    return res


def __execute(output_file, func, img, arg):
    img = func(img, arg)
    cv2.imwrite(output_file, img)
    plt.hist(img.ravel(), 256, (0, 256))
    plt.show()


def execute(files_map, globs, methods):
    for f in files_map:
        img = cv2.imread(f[0], cv2.IMREAD_GRAYSCALE)
        for g in globs:
            __execute(get_output_file_fullname(f[1], False, g), threshold_global, np.copy(img), g)
        for m in methods:
            __execute(get_output_file_fullname(f[1], True, m), threshold_local, np.copy(img), m)


def main():
    inputs, outputs, types, globs, methods = get_args(parse_args())
    files_map, _ = map_in_out(inputs, outputs, types)
    execute(files_map, globs, methods)


if __name__ == "__main__":
    main()
