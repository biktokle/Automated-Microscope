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


original_im = os.path.join(ROOT_PATH, 'example1.tif')
im = io.imread(original_im)
for i, image in enumerate(im):
    time.sleep(2)
    if image.shape[0] <= 3:
        image = image[1]
    frame = image
    # frame = np.dstack((np.zeros((len(image), len(image[0]))), image,  np.zeros((len(image), len(image[0])))))
    io.imsave(os.path.join(IMAGES_PATH, f'{i}.tif'), frame)

