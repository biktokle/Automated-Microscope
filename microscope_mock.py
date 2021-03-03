import time

import cv2
import imageio
import tifffile as tiff
import os
import numpy as np
from skimage import io
from definitions import global_vars, VARNAMES, ROOT_DIR


def image_to_8bit_equalized(image):
    ratio = np.amax(image) / 256
    img8 = (image / ratio).astype('uint8')

    return img8


original_im = os.path.join(ROOT_DIR, 'images', 'example.tiff')
im = io.imread(original_im)
for i, image in enumerate(im):
    time.sleep(1)

    frame = image_to_8bit_equalized(np.dstack((np.zeros((len(image[0]), len(image[0][0]))), image[1], image[0])))
    io.imsave(os.path.join(global_vars[VARNAMES.image_path.value], f'{i}.jpg'), frame)

