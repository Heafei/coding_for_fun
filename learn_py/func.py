import cv2
import numpy as np


def onMouse(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(y,x, buffer2[y,x])

methods = [
    ("cv2.INTER_NEAREST", cv2.INTER_NEAREST),
    ("cv2.INTER_LINEAR", cv2.INTER_LINEAR),
    ("cv2.INTER_AREA", cv2.INTER_AREA),
    ("cv2.INTER_CUBIC", cv2.INTER_CUBIC),
    ("cv2.INTER_LANCZOS4", cv2.INTER_LANCZOS4)]

class RawImage:
    def __init__(self):
        pass


def rawImageRead(file: str, width: int, height: int, dtype: np.dtype):
    # assert isinstance(file, str) and isinstance(width, int) and isinstance(height, int)
    bayerIn = np.fromfile(file, dtype, width*height)
    bayerIn.shape = height, width
    return bayerIn


raw_img = 'D:/Workspace/github/pixle_lab_py/data/Macbeth_TL84_Bright_3264x2448_8bits_GBRG.raw'
raw_img2 = 'D:/Workspace/github/pixle_lab_py/data/Macbeth_D65_4208x3120_10bits_GBGR.raw'
raw_dump = 'D:/Workspace/github/pixle_lab_py/data/Macbeth_TL84_Bright_3264x2448_8bits_GBRG.raw.txt'
shapeOut = (4208, 3120, 3)
# bayerBuffer = np.fromfile(raw_img, count=3264*2448, dtype=np.uint8)
# bayerBuffer.shape = 2448, 3264
# bayerBuffer = np.resize(bayerBuffer, shapeIn)
bayerBuffer = rawImageRead(raw_img, 3264, 2448, np.uint8)
buffer2 = rawImageRead(raw_img2, 4208, 3120, np.uint16)
# np.ndarray.tofile(bayerBuffer, raw_dump)

rgbBuffer = cv2.cvtColor(bayerBuffer, code=cv2.COLOR_BAYER_GB2BGR, dstCn=3)
img2 = cv2.cvtColor(buffer2, code=cv2.COLOR_BAYER_GR2BGR, dstCn=3)

imgShow = cv2.resize(rgbBuffer, (816, 612))
cv2.imwrite('t.jpeg', img2)
img2 = cv2.imread('t.jpeg')
cv2.imshow("ImageView", img2)
cv2.setMouseCallback('ImageView', onMouse)
cv2.waitKey(0)
#


