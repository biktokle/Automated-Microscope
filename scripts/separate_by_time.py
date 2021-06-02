import cv2
from skimage import io
import numpy as np
import os

SEPARATED = r'C:\Users\viktor_koukouliev\Downloads\fly spit images\separated'
PATH = r'C:\Users\viktor_koukouliev\Downloads\fly spit images\image.tif'

def image_to_8bit_equalized(image):
    ratio = np.amax(image) / 256
    img8 = (image / ratio).astype('uint8')

    return img8

img = io.imread(PATH)

for frame_num, image in enumerate(img[0::10]):

    frame = image_to_8bit_equalized(np.dstack((np.zeros((len(image[0]), len(image[0][0]))), image[1], image[0])))
    cv2.imwrite(os.path.join(SEPARATED, f'image_{frame_num}.jpg'), frame)




