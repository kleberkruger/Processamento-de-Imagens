import argparse
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
from imapp import ImageApp


def _transform(img, color=0):
    # return cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 254, 255, cv2.THRESH_BINARY)[1]
    img[cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) < 255] = color
    return img


def _contour(img, color=(0, 0, 0), thickness=1):
    print(color, thickness)
    new_img = np.zeros(img.shape)
    new_img.fill(255)
    _, thresh = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return cv2.drawContours(new_img, contours[1:len(contours) + 1], -1, color, thickness)


def _get_area(img, cnt):
    bx, by, bw, bh = cv2.boundingRect(cnt)
    src = img[by:by + bh, bx:bx + bw]
    src = cv2.threshold(cv2.cvtColor(src, cv2.COLOR_BGR2GRAY), 254, 255, cv2.THRESH_BINARY_INV)[1]
    return cv2.countNonZero(src)


def _property(img, centroide=True, perimetro=True, area=True):
    _, thresh = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[1:len(contours) + 1]
    contours.reverse()
    for i, c in enumerate(contours):
        m = cv2.moments(c)
        cx = int(m['m10'] / m['m00'])
        cy = int(m['m01'] / m['m00'])
        area = cv2.contourArea(c)
        perimeter = cv2.arcLength(c, True)
        _, axes, _ = cv2.fitEllipse(c)
        ecc = np.sqrt(1 - (min(axes) / max(axes)) ** 2)
        sol = area / float(cv2.contourArea(cv2.convexHull(c)))
        cv2.putText(img, str(i), (cx - 2, cy + 2), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 0), 1)
        print("região {}: área: {} perímetro: {} excentricidade: {} solidez: {}".format(i, area, perimeter, ecc, sol))
    return img


def __get_classification(area, ranges=(1500, 3000)):
    return 0 if area < 1500 else 1 if area < 3000 else 2


def _calc_histogram(img, ranges=(1500, 3000)):
    _, thresh = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[1:len(contours) + 1]
    regions = [0] * (len(ranges) + 1)
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        regions[__get_classification(area)] += 1
    return regions


def _generate_histogram(data):
    x = np.arange(3)
    fig, ax = plt.subplots()
    plt.bar(x, data)
    plt.xticks(x, ('Pequenos', 'Médios', 'Grandes'))
    return plt


def _histogram(outfile, img, ranges=(1500, 3000)):
    plt = _generate_histogram(_calc_histogram(img, ranges))
    plt.savefig(outfile)


def _execute_and_save(out_path, func, *args):
    response = func(*args)
    cv2.imwrite(out_path, response)


def _required_length(nmin, nmax):
    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not nmin <= len(values) <= nmax:
                msg = 'argument "{f}" requires between {nmin} and {nmax} arguments'.format(
                    f=self.dest, nmin=nmin, nmax=nmax)
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, values)

    return RequiredLength


def _get_args(args):
    f = args.transform if args.transform is None or args.transform else [0]
    c = args.contour if args.contour is None or args.contour else [0, 0, 255, 1]
    p = args.property if args.property is None or args.property else 'all'
    g = args.hist if args.hist is None or args.hist else [1500, 3000]
    return f, c, p, g


def _get_arg_contour(arg):
    if len(arg) == 1:
        return arg[0], 1
    elif len(arg) == 2:
        return arg[0], arg[1]
    elif len(arg) == 3:
        return arg
    elif len(arg) == 4:
        return arg[0:3], arg[3]


class ObjectsApp(ImageApp):

    def __init__(self):
        super().__init__()

    def _add_arguments(self, parser):
        parser.add_argument('-f', '--transform', type=int, nargs='*', action=_required_length(0, 1),
                            help='color transformation')
        parser.add_argument('-c', '--contour', type=int, nargs='*', action=_required_length(0, 4),
                            help='contour objects')
        parser.add_argument('-p', '--property', type=str, nargs='*', choices=['all', 'c', 'p', 'a'],
                            help='extract object properties')
        parser.add_argument('-g', '--hist', '--histogram', type=int, nargs='*', help='object histogram')

    def _execute(self, paths, args):
        f, c, p, g = _get_args(args)
        img = cv2.imread(paths.in_path)
        filename = os.path.splitext(paths.out_path)[0]
        if f is not None:
            _execute_and_save('{}-{}.png'.format(filename, 'transform'), _transform, np.copy(img), f)
        if c is not None:
            _execute_and_save('{}-{}.png'.format(filename, 'contour'), _contour, np.copy(img), *_get_arg_contour(c))
        if p is not None:
            _execute_and_save('{}-{}.png'.format(filename, 'property'), _property, np.copy(img), p)
        if g is not None:
            _histogram('{}-{}.png'.format(filename, 'histogram'), np.copy(img), g)


if __name__ == '__main__':
    ObjectsApp().start()

    # img = cv2.imread('in/objetos1.png')
    # _execute_and_save('out/transform-obj1.png', _transform, np.copy(img), 0)
    # _execute_and_save('out/contour-obj1.png', _contour, np.copy(img), (0, 0, 255), 1)
    # _execute_and_save('out/property-obj1.png', _property, np.copy(img))
    # _execute_and_save('out/histogram-obj1.png', _histogram, np.copy(img))

    # img = cv2.imread('in/objetos2.png')
    # _execute_and_save('out/transform-obj2.png', _transform, np.copy(img), 0)
    # _execute_and_save('out/contour-obj2.png', _contour, np.copy(img), (0, 0, 255), 1)
    # _execute_and_save('out/property-obj2.png', _property, np.copy(img))
    # _execute_and_save('out/histogram-obj2.png', _histogram, np.copy(img))

    # img = cv2.imread('in/objetos3.png')
    # _execute_and_save('out/transform-obj3.png', _transform, np.copy(img), 0)
    # _execute_and_save('out/contour-obj3.png', _contour, np.copy(img), (0, 0, 255), 1)
    # _execute_and_save('out/property-obj3.png', _property, np.copy(img))
    # _execute_and_save('out/histogram-obj3.png', _histogram, np.copy(img))
