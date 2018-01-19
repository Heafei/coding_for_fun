import cv2
import numpy as np
import sys


class ImageViewer:
    def __init__(self, image: np.ndarray):
        self.img = image
        self.gamma = 1.0
        if len(image.shape) > 2:
            self.type = 'color'
        else:
            self.type = 'gray'
        self.view_size = (600, 800)
        self.__x1 = 0
        self.__y1 = 0
        self.__x2 = 0
        self.__y2 = 0
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
        if event == cv2.EVENT_LBUTTONDOWN:
            self.__x1, self.__y1 = x, y
        if event == cv2.EVENT_LBUTTONUP:
            self.__x2, self.__y2 = x, y
            self.get_roi()

    def get_roi(self):
        x_lt, x_rb = (self.__x1, self.__x2) if self.__x2 > self.__x1 else (self.__x2, self.__x1)
        y_lt, y_rb = (self.__y1, self.__y2) if self.__y2 > self.__y1 else (self.__y2, self.__y1)
        img = np.array(self.view_img)
        # print(x_lt, y_lt,x_rb,y_rb)
        roi: np.ndarray = img[y_lt:y_rb, x_lt:x_rb, :]
        b,g,r = self.average_rgb(roi)
        print('r={:3.04f}, g={:3.04f}, b={:3.04f}'.format(r, g, b))
        print('r/g={:2.04f}, b/g={:2.04f}, b/r={:2.04f}'.format(r/g, b/g, b/r))
        rois = self.get_color_checker_rois(roi)
        for idx, r in enumerate(rois):
            print(idx+1, self.average_rgb(r))
        cv2.rectangle(img, (x_lt, y_lt), (x_rb, y_rb), (0, 0, 255))
        cv2.imshow('Image', img)
        return roi

    def get_color_checker_rois(self, roi):
        height, width = roi.shape[:2]
        h, w = int(height/4), int(width/6)
        h_offset, w_offset = int(h/4), int(w/4)
        rois = []
        for row in range(4):
            for col in range(6):
                x_lt = w*col + w_offset
                y_lt = h*row + h_offset
                x_rb = x_lt + 2*w_offset
                y_rb = y_lt + 2*h_offset
                tile = np.array(roi[y_lt:y_rb, x_lt:x_rb])
                rois.append(tile)
                cv2.rectangle(roi, (x_lt, y_lt), (x_rb, y_rb), (0,0,255))
        # cv2.circle(roi, (int(width/2), int(height/2)), 10, (0, 0, 255), -1)
        return rois


    def average_rgb(self, roi: np.ndarray):
        r_mean = np.mean(roi[:, :, 2])
        g_mean = np.mean(roi[:, :, 1])
        b_mean = np.mean(roi[:, :, 0])
        return b_mean, g_mean, r_mean

    def show(self, window_name: str='Image'):
        cv2.namedWindow(window_name)

        cv2.imshow(window_name, self.view_img)
        # cv2.resizeWindow(window_name, self.view_size[0], self.view_size[1])
        cv2.setMouseCallback(window_name, self.on_mouse)
        cv2.waitKey(0)
        del self


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        exit(-1)
    img = cv2.imread(sys.argv[1])
    if img is None:
        exit(-1)
    ImageViewer(img).show()