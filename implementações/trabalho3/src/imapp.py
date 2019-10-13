import argparse
import abc
import os
import sys
import glob
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


def __select_argument(arg_base, arg_opt, def_value):
    return arg_opt if arg_opt is not None else [arg_base] if arg_base is not None else def_value


def _unpack_args(args):
    inputs = [str(Path(i)) for i in __select_argument(args.input, args.input_o, [__DEFAULT_ARG_IN])]
    outputs = __select_argument(args.output, args.output_o, None)
    if outputs is not None:
        if len(outputs) != 1 and len(outputs) != len(inputs):
            raise Exception("number of <input> is not correspond to <output>")
        outputs = [outputs[0]] * len(inputs) if len(outputs) < len(inputs) else outputs
    else:
        outputs = inputs if args.input_o is not None or args.input is not None else [__DEFAULT_ARG_OUT]
    return inputs, [str(Path(o)) for o in outputs]


def __get_images_in_directory(dir_path, extensions='*'):
    if extensions == '*':
        extensions = __ALL_EXTENSIONS
    image_paths = []
    for ext in extensions:
        image_paths += [f for f in glob.glob(dir_path + "**/" + ext, recursive=False)]
    return image_paths


def __get_output_file_name(in_img, output):
    return output + '/' + Path(in_img).name


def _get_image_paths(args):
    inputs, outputs = _unpack_args(args)
    paths = []
    for i, f in enumerate(inputs):
        if not os.path.exists(f):
            print("input '{}' not exists".format(f), file=sys.stderr)
        elif os.path.isdir(f):
            for g in __get_images_in_directory(f, args.type):
                paths.append(InOutPath(g, __get_output_file_name(g, outputs[i])))
        else:
            paths.append(InOutPath(f, __get_output_file_name(f, outputs[i])))
    return paths


class InOutPath:
    def __init__(self, in_path, out_path):
        self.in_path = in_path
        self.out_path = out_path

    def __str__(self):
        return "[in='" + self.in_path + "', out='" + self.out_path + "')"


class ImageApp(abc.ABC):

    def __init__(self):
        self._args = self._parse_args()
        self._paths = _get_image_paths(self._args)
        del self._args.input, self._args.input_o, self._args.output, self._args.output_o, self._args.type

    @abc.abstractmethod
    def _add_arguments(self, parser): pass

    @abc.abstractmethod
    def _execute(self, paths, args): pass

    def _parse_args(self):
        parser = argparse.ArgumentParser()
        _add_default_arguments(parser)
        self._add_arguments(parser)
        return parser.parse_args()

    def start(self):
        for paths in self._paths:
            self._execute(paths, self._args)
