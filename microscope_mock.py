import time
import os
import numpy as np
from skimage import io


IMAGES_PATH = r'C:\Users\viktor_koukouliev\Desktop\WORKDIR\images'
ROOT_PATH = r'C:\Users\viktor_koukouliev\Desktop\WORKDIR'


def image_to_8bit_equalized(image):
    ratio = np.amax(image) / 256
    img8 = (image / ratio).astype('uint8')

    return img8


original_im = os.path.join(ROOT_PATH, 'example.tif')
im = io.imread(original_im)
for i, image in enumerate(im):
    time.sleep(1)
    frame = np.dstack((np.zeros((len(image[0]), len(image[0][0]))), image[1], image[0]))
    io.imsave(os.path.join(IMAGES_PATH, f'{i}.tif'), frame)

