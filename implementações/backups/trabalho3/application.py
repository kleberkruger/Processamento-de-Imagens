import argparse
import abc
import os
import glob
import sys
from pathlib import Path

__DEFAULT_ARG_IN = 'in'
__DEFAULT_ARG_OUT = 'out'
__ALL_EXTENSIONS = (
    '*.bitmap', '*.gif', '*.jpeg', '*.pbm', '*.pgm', '*.png', '*.pnm', '*.ppm', '*.raw', '*.tiff', '*.svg'
)


def _add_default_arguments(parser):
    in_group = parser.add_mutually_exclusive_group()
    in_group.add_argument('input', type=str, nargs='?', help="input-file or input-dir")
    in_group.add_argument('-i', '--in', '--input', type=str, nargs='+', dest='input_o',
                          help='input-file or input-dir')
    out_group = parser.add_mutually_exclusive_group()
    out_group.add_argument('output', type=str, nargs='?', help="output-file or output-dir")
    out_group.add_argument('-o', '--out', '--output', type=str, nargs='+', dest='output_o',
                           help='output-file or output-dir')
    parser.add_argument('-t', '--type', type=str, nargs='+', default='*',
                        help='image extension type to scan within a directory')


def __get_images_in_directory(dir_path, extensions='*'):
    if extensions == '*':
        extensions = __ALL_EXTENSIONS
    image_paths = []
    for ext in extensions:
        image_paths += [f for f in glob.glob(dir_path + "**/" + ext, recursive=False)]
    return image_paths


def __get_default_filename(out, filename):
    return out + '/' + filename if os.path.isdir(out) else out


def __get_args(args):
    inputs = [str(Path(i)) for i in args.input_o] if args.input_o is not None \
        else [str(Path(args.input))] if args.input is not None else [__DEFAULT_ARG_IN]
    out = args.output_o if args.output_o is not None else [args.output] if args.output is not None else None

    if out is not None:
        if len(out) != 1 and len(out) != len(inputs):
            raise Exception("number of <input> is not correspond to <output>")
        return (inputs, [str(Path(out[0]))] * len(inputs)) if len(out) < len(inputs) \
            else (inputs, [str(Path(o)) for o in out])

    return (inputs, inputs) if args.input_o is not None else (inputs, [args.input]) if args.input is not None \
        else (inputs, [__DEFAULT_ARG_OUT])


def _unpack_args(args):
    inputs, outputs = __get_args(args)
    print(inputs, outputs)

    file_paths = []
    for i in range(len(inputs)):
        fin = inputs[i]
        if not os.path.exists(fin):
            print("input '{}' not exists".format(fin), file=sys.stderr)
        elif os.path.isdir(fin):
            for f in __get_images_in_directory(fin, args.type):
                file_paths.append(InOutPath(f, __get_default_filename(outputs[i], f)))
        else:
            file_paths.append(InOutPath(fin, __get_default_filename(outputs[i], fin)))
    return file_paths


class InOutPath:
    def __init__(self, in_path, out_path):
        self.in_path = in_path
        self.out_path = out_path


class Application(abc.ABC):

    @abc.abstractmethod
    def _add_arguments(self, parser): pass

    @abc.abstractmethod
    def _get_default_file_fullname(self, filename): pass

    def _parse_args(self):
        parser = argparse.ArgumentParser()
        _add_default_arguments(parser)
        self._add_arguments(parser)
        args = parser.parse_args()
        files = _unpack_args(args)
        for f in files:
            print(f.in_path, f.out_path)
        del args.input, args.output, args.input_o, args.output_o, args.type
        return args

    def __init__(self):
        self._args = self._parse_args()

    def start(self):
        print(self._args)
