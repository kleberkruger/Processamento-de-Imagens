import argparse
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
from imapp import ImageApp


class Contour:
    ''' Provides detailed parameter informations about a contour

        Create a Contour instant as follows: c = Contour(src_img, contour)
                where src_img should be grayscale image.

        Attributes:

        c.area -- gives the area of the region
        c.parameter -- gives the perimeter of the region
        c.moments -- gives all values of moments as a dict
        c.centroid -- gives the centroid of the region as a tuple (x,y)
        c.bounding_box -- gives the bounding box parameters as a tuple => (x,y,width,height)
        c.bx,c.by,c.bw,c.bh -- corresponds to (x,y,width,height) of the bounding box
        c.aspect_ratio -- aspect ratio is the ratio of width to height
        c.equi_diameter -- equivalent diameter of the circle with same as area as that of region
        c.extent -- extent = contour area/bounding box area
        c.convex_hull -- gives the convex hull of the region
        c.convex_area -- gives the area of the convex hull
        c.solidity -- solidity = contour area / convex hull area
        c.center -- gives the center of the ellipse
        c.majoraxis_length -- gives the length of major axis
        c.minoraxis_length -- gives the length of minor axis
        c.orientation -- gives the orientation of ellipse
        c.eccentricity -- gives the eccentricity of ellipse
        c.filledImage -- returns the image where region is white and others are black
        c.filledArea -- finds the number of white pixels in filledImage
        c.convexImage -- returns the image where convex hull region is white and others are black
        c.pixelList -- array of indices of on-pixels in filledImage
        c.maxval -- corresponds to max intensity in the contour region
        c.maxloc -- location of max.intensity pixel location
        c.minval -- corresponds to min intensity in the contour region
        c.minloc -- corresponds to min.intensity pixel location
        c.meanval -- finds mean intensity in the contour region
        c.leftmost -- leftmost point of the contour
        c.rightmost -- rightmost point of the contour
        c.topmost -- topmost point of the contour
        c.bottommost -- bottommost point of the contour
        c.distance_image((x,y)) -- return the distance (x,y) from the contour.
        c.distance_image() -- return the distance image where distance to all points on image are calculated
        '''

    def __init__(self, img, cnt):
        self.img = img
        self.cnt = cnt
        self.size = len(cnt)

        # MAIN PARAMETERS

        # Contour.area - Area bounded by the contour region'''
        self.area = cv2.contourArea(self.cnt)

        # contour perimeter
        self.perimeter = cv2.arcLength(cnt, True)

        # centroid
        self.moments = cv2.moments(cnt)
        if self.moments['m00'] != 0.0:
            self.cx = self.moments['m10'] / self.moments['m00']
            self.cy = self.moments['m01'] / self.moments['m00']
            self.centroid = (self.cx, self.cy)
        else:
            self.centroid = "Region has zero area"

        # bounding box
        self.bounding_box = cv2.boundingRect(cnt)
        (self.bx, self.by, self.bw, self.bh) = self.bounding_box

        # aspect ratio
        self.aspect_ratio = self.bw / float(self.bh)

        # equivalent diameter
        self.equi_diameter = np.sqrt(4 * self.area / np.pi)

        # extent = contour area/boundingrect area
        self.extent = self.area / (self.bw * self.bh)

        ### CONVEX HULL ###

        # convex hull
        self.convex_hull = cv2.convexHull(cnt)

        # convex hull area
        self.convex_area = cv2.contourArea(self.convex_hull)

        # solidity = contour area / convex hull area
        self.solidity = self.area / float(self.convex_area)

        ### ELLIPSE  ###

        self.ellipse = cv2.fitEllipse(cnt)

        # center, axis_length and orientation of ellipse
        (self.center, self.axes, self.orientation) = self.ellipse

        # length of MAJOR and minor axis
        self.majoraxis_length = max(self.axes)
        self.minoraxis_length = min(self.axes)

        # eccentricity = sqrt( 1 - (ma/MA)^2) --- ma= minor axis --- MA= major axis
        self.eccentricity = np.sqrt(1 - (self.minoraxis_length / self.majoraxis_length) ** 2)

        ### CONTOUR APPROXIMATION ###

        self.approx = cv2.approxPolyDP(cnt, 0.02 * self.perimeter, True)

        ### EXTRA IMAGES ###

        # filled image :- binary image with contour region white and others black
        self.filledImage = np.zeros(self.img.shape[0:2], np.uint8)
        cv2.drawContours(self.filledImage, [self.cnt], 0, 255, -1)

        # area of filled image
        self.filledArea = cv2.countNonZero(self.filledImage)

        # pixelList - array of indices of contour region
        self.pixelList = np.transpose(np.nonzero(self.filledImage))

        # convex image :- binary image with convex hull region white and others black
        self.convexImage = np.zeros(self.img.shape[0:2], np.uint8)
        cv2.drawContours(self.convexImage, [self.convex_hull], 0, 255, -1)

        ### PIXEL PARAMETERS

        # mean value, minvalue, maxvalue
        # self.minval, self.maxval, self.minloc, self.maxloc = cv2.minMaxLoc(self.img, mask=self.filledImage)
        # self.meanval = cv2.mean(self.img, mask=self.filledImage)

        ### EXTREME POINTS ###

        # Finds the leftmost, rightmost, topmost and bottommost points
        self.leftmost = tuple(self.cnt[self.cnt[:, :, 0].argmin()][0])
        self.rightmost = tuple(self.cnt[self.cnt[:, :, 0].argmax()][0])
        self.topmost = tuple(self.cnt[self.cnt[:, :, 1].argmin()][0])
        self.bottommost = tuple(self.cnt[self.cnt[:, :, 1].argmax()][0])
        self.extreme = (self.leftmost, self.rightmost, self.topmost, self.bottommost)


class Object:

    def __init__(self, cnt):
        self.cnt = cnt

        # Contour.area - Area bounded by the contour region'''
        self.area = cv2.contourArea(self.cnt)

        # contour perimeter
        self.perimeter = cv2.arcLength(cnt, True)

        # centroid
        self.moments = cv2.moments(cnt)
        if self.moments['m00'] != 0.0:
            self.cx = self.moments['m10'] / self.moments['m00']
            self.cy = self.moments['m01'] / self.moments['m00']
            self.centroid = (self.cx, self.cy)
        else:
            self.centroid = "Region has zero area"

        # convex hull
        self.convex_hull = cv2.convexHull(cnt)

        # convex hull area
        self.convex_area = cv2.contourArea(self.convex_hull)

        # solidity = contour area / convex hull area
        self.solidity = self.area / float(self.convex_area)

        self.ellipse = cv2.fitEllipse(cnt)
        # center, axis_length and orientation of ellipse
        (self.center, self.axes, self.orientation) = self.ellipse

        # length of MAJOR and minor axis
        self.major_axis_length = max(self.axes)
        self.minor_axis_length = min(self.axes)

        # eccentricity = sqrt( 1 - (ma/MA)^2) --- ma= minor axis --- MA= major axis
        self.eccentricity = np.sqrt(1 - (self.minor_axis_length / self.major_axis_length) ** 2)


def _transform(img, color=0):
    # return cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 254, 255, cv2.THRESH_BINARY)[1]
    img[cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) < 255] = color
    return img


def _contour(img, color=(0, 0, 0), thickness=1):
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
        # print(_get_area(img, c))
        # obj = Object(c)
        # print("região {}: área: {} perímetro: {} excentricidade: {} solidez: {}".format(
        #     i, obj.area, obj.perimeter, obj.eccentricity, obj.solidity))
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
    plt.show()


def _histogram(img, ranges=(1500, 3000)):
    return _generate_histogram(_calc_histogram(img, ranges))


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
        parser.add_argument('-p', '--property', type=str, nargs='+', choices=['all', 'c', 'p', 'a'],
                            help='extract object properties')
        parser.add_argument('-g', '--hist', '--histogram', type=int, nargs='*', help='object histogram')

    def _execute(self, paths, args):
        f, c, p, g = _get_args(args)
        # img = cv2.imread('in/objetos1.png')
        if f is not None:
            print(f)
        if c is not None:
            print(_get_arg_contour(c))
        if p is not None:
            print(p)
        if g is not None:
            print(g)

        # img = cv2.imread(paths.in_path)
        # filename = os.path.splitext(paths.out_path)[0]
        # print(filename, args.transform, args.contour)
        # for v in [args.transform]:
        #     _execute_and_save('{}-{}.png'.format(filename, 't'), _transform, np.copy(img), v)
        # for v in args.contour:
        #     _execute_and_save('{}-{}.png'.format(filename, 'c'), _contour, np.copy(img), v)
        # for v in args.property:
        #     _execute_and_save('{}-{}.png'.format(filename, 'p'), _property, np.copy(img), v)
        # for v in [args.hist]:
        #     _execute_and_save('{}-{}.png'.format(filename, 'h'), _hist, np.copy(img), v)


if __name__ == '__main__':
    # ObjectsApp().start()
    img = cv2.imread('in/objetos3.png')
    # # _execute_and_save('out/teste.png', _contour, np.copy(img), (0, 0, 255), 1)
    _execute_and_save('out/teste.png', _property, np.copy(img))
    # _execute_and_save('out/teste.png', _histogram, np.copy(img))
    # _histogram(img)

    # src = cv2.imread('in/objetos3.png', 0)
    # binary_map = (src > 0).astype(np.uint8)
    # connectivity = 4
    # output = cv2.connectedComponentsWithStats(binary_map, connectivity, cv2.CV_32S)
    # # The first cell is the number of labels
    # num_labels = output[0]
    # # The second cell is the label matrix
    # labels = output[1]
    # # The third cell is the stat matrix
    # stats = output[2]
    # # The fourth cell is the centroid matrix
    # centroids = output[3]
    # print(num_labels, labels, stats, centroids)
