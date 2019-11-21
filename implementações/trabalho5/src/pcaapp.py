from imapp import ImageApp
import cv2
import numpy as np
from scipy.linalg import svd


def _pca(img, k):
    Uf = [None] * img.shape[2]
    Sf = [None] * img.shape[2]
    Vf = [None] * img.shape[2]

    for i in range(img.shape[2]):
        Uf[i], Sf[i], Vf[i] = svd(img[:, :, i])

    g = np.zeros((img.shape[0], img.shape[1], img.shape[2]))
    Ug = Uf.copy()
    Sg = Sf.copy()
    Vg = Vf.copy()

    for i in range(img.shape[2]):
        Ug[i][:, 1: k] = Uf[i][:, 1:k]
        Sg[i][1:k, :] = Sf[i][1:k, 1:k]
        Vg[i][1:k, :] = np.transpose(Vf[1:k:i])
        g[:, :, i] = Ug[i][:, :] * Sg[:, :] * Vg[i][:, :]

    return g


class PCAApp(ImageApp):

    def __init__(self):
        super().__init__()

    def _add_arguments(self, parser):
        parser.add_argument('-k', '--component', type=int, nargs='*', help='number of components')

    def _execute(self, paths, args):
        print(paths, args)
        img = cv2.imread(paths.in_path)
        _pca(img, args.component)


if __name__ == '__main__':
    PCAApp().start()
