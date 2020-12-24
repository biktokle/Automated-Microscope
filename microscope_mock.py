import time
import tifffile as tiff
import os
from definitions import global_vars, VARNAMES, ROOT_DIR

original_im = os.path.join(ROOT_DIR, 'images', 'example.tiff')

for i in range(10):
    time.sleep(1)
    im = tiff.imread(original_im)
    tiff.imsave(os.path.join(global_vars[VARNAMES.image_path.value], f'{i}.tiff'), im)

