import cv2
import sys
import numpy as np


def dump_rgb565_to_file(file: str, txt: int=0):
    img_bgr = cv2.imread(file)
    print('Opening image :', file)
    if img_bgr is None:
        print("fail opening image : {}".format(file))
        return -1
    img_rgb = img_bgr[:, :, ::-1]
    dump_file = file + '.txt'
    dump_bin = file + '.bin'
    fp_txt = open(dump_file, 'w')
    fp_bin = open(dump_bin, 'wb')
    if fp_bin is None or fp_txt is None:
        print("error")
        return -1

    img_rgb565 = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2BGR565)
    print(img_rgb565.shape)
    rows, cols = img_rgb565.shape[:2]
    print('rgb-(0,0)',img_rgb[0, 0])
    print('bgr-(0,0)', img_bgr[0, 0])
    for row in range(rows):
        for col in range(cols):
            rgb565_pixel_str = '0x{:02x}{:02x} '.format(img_rgb565[row, col, 0], img_rgb565[row, col, 1])
            rgb565_pixel_hex = (img_rgb565[row, col, 0] << 8) | img_rgb565[row, col, 1]
            fp_txt.write(rgb565_pixel_str)
            fp_bin.write(np.uint16(rgb565_pixel_hex))
        fp_txt.write('\n')
        # fp_bin.write('\n')
    fp_bin.close()
    fp_txt.close()
    return 0


if __name__ == '__main__':
    if not (len(sys.argv) == 2):
        print("Usage: python dump_rgb565.py image_file_path")
        exit()
    dump_rgb565_to_file(sys.argv[1])
