""" doc

"""

__version__ = '0.1'
__author__ = "heafei@aliyun.com"

import cv2
from enum import Enum, unique
import numpy as np

@unique
class BayerPattern(Enum):
    BAYER_GR = 0
    BAYER_R  = 1
    BAYER_B  = 2
    BAYER_GB = 3


def read_raw_image(file: str, shape: tuple, dtype: np.dtype, pattern: Enum = BayerPattern.BAYER_GB):
    # assert isinstance(file, str) and isinstance(width, int) and isinstance(height, int)
    width, height = shape[0], shape[1]
    bayer_in = np.fromfile(file, dtype, width * height)
    bayer_in.shape = (height, width)
    return RawImage(bayer_in, pattern)


class RawImage:
    def __init__(self, img: np.ndarray, pattern: Enum):
        self.bayer_pattern = pattern
        self.buffer: np.ndarray = img
        self.wb_gain = (1.0, 1.0, 1.0)  # (r_gain, g_gain, b_gain)

    def to_rgb(self):
        code = {BayerPattern.BAYER_GB: cv2.COLOR_BAYER_GB2BGR,
                BayerPattern.BAYER_R: cv2.COLOR_BAYER_RG2BGR,
                BayerPattern.BAYER_B: cv2.COLOR_BAYER_BG2BGR,
                BayerPattern.BAYER_GR: cv2.COLOR_BAYER_GR2BGR}
        print(code[self.bayer_pattern])
        return cv2.cvtColor(self.buffer, code[self.bayer_pattern], dstCn=3)

    def white_balance_apply(self):
        # todo
        pass

    def white_balance_calc(self):
        pass
        # todo


def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

class ImageViewer:
    def __init__(self, image: np.ndarray):
        self.img = image
        self.gamma = 1.0
        if len(image.shape) > 2:
            self.type = 'color'
        else:
            self.type = 'gray'
        self.view_size = (600, 800)
        if self.view_size[0] < image.shape[1] or self.view_size[1] > image.shape[0]:
            self.view_img = self.__scale((800, 600))
            print(self.view_img.shape)
            print(self.img.shape)

    def __scale(self, size):
        view_w, view_h = size[0], size[1]
        img_w, img_h = self.img.shape[1], self.img.shape[0]
        if view_h < img_h:
            dsize = (int(view_h/img_h*img_w), view_h)
            return cv2.resize(self.img, dsize)
        else:
            return self.img

    def on_mouse(self, event, x, y, flag, param):
        if event == cv2.EVENT_LBUTTONUP:
            print(x, y, '=', self.img[y, x])


    def show(self, window_name: str='Image'):
        cv2.namedWindow(window_name)

        cv2.imshow(window_name, self.view_img)
        # cv2.resizeWindow(window_name, self.view_size[0], self.view_size[1])
        cv2.setMouseCallback(window_name, self.on_mouse)
        cv2.waitKey(0)
        del self


path = 'D:\Workspace\github\coding_for_fun\pixle_lab_py\data\Macbeth_TL84_Bright_3264x2448_8bits_GBRG.raw'
shape = (3264, 2448)
dtype = np.uint8
pattern = BayerPattern.BAYER_GB
raw_image = read_raw_image(path, shape, dtype, pattern)
ImageViewer(raw_image.to_rgb()).show()
