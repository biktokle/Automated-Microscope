import time
import tifffile as tiff
import os
from definitions import global_vars, VARNAMES

original_im = r'C:\Users\vkoukoul\PycharmProjects\Automated-Microscope\images\\example.tiff'

for i in range(10):
    time.sleep(1)
    im = tiff.imread(original_im)
    tiff.imsave(os.path.join(global_vars[VARNAMES.image_path.value], f'{i}.tiff'), im)

