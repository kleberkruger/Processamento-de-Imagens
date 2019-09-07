import argparse
import cv2
import numpy as np
import os


class ImageSet:
    def __init__(self, infile, outfile, mask, direction):
        self.infile = infile
        self.outfile = outfile
        self.mask = mask
        self.direction = direction


MASKS = [
    [
        [None, 0, 7 / 16],
        [3 / 16, 5 / 16, 1 / 16]
    ],
    [
        [None, None, None, 0, None, 32 / 200, None],
        [12 / 200, None, 26 / 200, None, 30 / 200, None, 16 / 200],
        [None, 12 / 200, None, 26 / 200, None, 12 / 200, None],
        [5 / 200, None, 12 / 200, None, 12 / 200, None, 5 / 200]
    ],
    [
        [None, None, 0, 8 / 32, 4 / 32],
        [2 / 32, 4 / 32, 8 / 32, 4 / 32, 2 / 32]
    ],
    [
        [None, None, 0, 5 / 32, 3 / 32],
        [2 / 32, 4 / 32, 5 / 32, 4 / 32, 2 / 32],
        [None, 2 / 32, 3 / 32, 2 / 32, None]
    ],
    [
        [None, None, 0, 8 / 42, 4 / 42],
        [2 / 42, 4 / 42, 8 / 42, 4 / 42, 2 / 42],
        [1 / 42, 2 / 42, 4 / 42, 2 / 42, 1 / 42]
    ],
    [
        [None, None, 0, 7 / 48, 5 / 48],
        [3 / 48, 5 / 48, 7 / 48, 5 / 48, 3 / 48],
        [1 / 48, 3 / 48, 5 / 48, 3 / 48, 1 / 48]
    ]
]


def parse_args():
    parser = argparse.ArgumentParser()

    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('input', type=str, nargs='?', default='in', help="input-file or input-dir")
    input_group.add_argument('-i', '--in', '--input', type=str, nargs='+', dest='input_o',
                             help='input-file or input-dir')

    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument('output', type=str, nargs='?', default='out', help="output-file or output-dir")
    output_group.add_argument('-o', '--out', '--output', type=str, nargs='+', dest='output_o',
                              help='output-file or output-dir')

    parser.add_argument('-m', '--mask', type=int, nargs='+', choices=[0, 1, 2, 3, 4, 5, 6], default=[0], help='mask')
    parser.add_argument('-d', '--direction', type=int, nargs='+', choices=[0, 1, 2], default=[0], help='direction')
    parser.add_argument('-c', '--color', type=int, nargs='+', choices=[0, 1, 2], default=[1], help='color map')

    args = parser.parse_args()
    return [args.input] if args.input_o is None else args.input_o, \
           [args.output] if args.output_o is None else args.output_o, args.mask, args.direction


def percurso_convencional(matriz, func):
    for y in range(len(matriz)):
        for x in range(len(matriz[y])):
            func(matriz, y, x)
        print()


def percurso_alternado(matriz, func):
    for y in range(len(matriz)):
        if y % 2 == 0:
            for x in range(len(matriz[y])):
                func(matriz, y, x)
            print()
        else:
            for x in range(len(matriz[y]) - 1, -1, -1):
                func(matriz, y, x)
            print()


def execute(in_img, out_img, mask, direction):
    print(in_img, out_img, mask, direction)
    for i in range(len(MASKS)):
        print("Mask", i)
        print(MASKS[i])


def main():
    inputs, outputs, masks, directions = parse_args()

    if len(outputs) != 1 and len(outputs) != len(inputs):
        raise Exception('Número de parâmetros inválido para --output')

    if len(inputs) > 0 and len(outputs) == 1:
        # FIXME: e o caso im1.png im2.png im3.png im1_out.png?
        outputs = [outputs[0]] * len(inputs)

    # print(inputs)
    # print(outputs)
    # print(masks)
    # print(directions)

    # TODO: Encontrar imagens dentro de uma pasta

    for i in range(len(inputs)):
        for mask in masks:
            for direction in directions:
                execute(inputs[i], outputs[i], mask, direction)


def imprimir(matriz, y, x):
    print(matriz[y][x], end=" ")


m = np.arange(12).reshape((3, 4))
percurso_convencional(m, imprimir)
print()
percurso_alternado(m, imprimir)

# main()
