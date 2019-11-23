from imapp import ImageApp
import numpy as np
import cv2
import os


def pca(img, k=64):
    g = np.zeros(img.shape)
    for i in range(img.shape[2]):
        u, s, v = np.linalg.svd(img[:, :, i], full_matrices=False)
        g[:, :, i] = np.dot(np.dot(u[:, :k], np.diag(s)[:k, :k]), v[:k, :])

    return g


def get_compression_rate(input_path, output_path):
    return os.stat(output_path).st_size / os.stat(input_path).st_size


def get_rmse(input_img, output_img):
    diff = input_img - output_img
    sqrt_error = (diff ** 2).sum()
    h, w, _ = input_img.shape
    return (sqrt_error / (h * w)) ** (1 / 5)


def _get_report_path(path):
    return 'report.txt' if path is None else path


def _write_in_report(report_path, msg):
    f = open(report_path, 'a')
    f.write(msg)
    f.close()


class PCAApp(ImageApp):

    def __init__(self):
        super().__init__()

    def _add_arguments(self, parser):
        parser.add_argument('-k', '--component', type=int, help='number of components')
        parser.add_argument('-r', '--report', type=str, help='report path')

    def _execute(self, paths, args):
        img = cv2.imread(paths.in_path)
        res = pca(img, args.component)
        cv2.imwrite(paths.out_path, res)
        cr = get_compression_rate(paths.in_path, paths.out_path)
        rmse = get_rmse(img, res)
        msg = 'input file: {}\toutput file:{}\ncompression_rate: {}\tRMSE: {}\n'.format(
            paths.in_path, paths.out_path, round(cr, 2), round(rmse, 2))

        _write_in_report(_get_report_path(args.report), msg)
        print(msg)


if __name__ == '__main__':
    PCAApp().start()
