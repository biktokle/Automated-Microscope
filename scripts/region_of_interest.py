import os
from skimage import io
import cv2
import numpy as np


SEPARATED = r'C:\Users\viktor_koukouliev\Downloads\fly spit images\separated'
DARKENED = r'C:\Users\viktor_koukouliev\Downloads\fly spit images\darkened'
SLICED = r'C:\Users\viktor_koukouliev\Downloads\fly spit images\sliced'
REGIONS = r'C:\Users\viktor_koukouliev\Downloads\fly spit images\regions.txt'
IMAGE_SIZE = (1200, 1200)

def read_regions(regions):
    all_text = open(regions).read()
    rows = all_text.split('\n')
    boxes = []
    for row in rows:
        if row == '':
            continue
        vals = row.split(',')
        corner1 = (int(vals[0]), int(vals[1]))
        corner2 = (int(vals[2]), int(vals[3]))
        boxes.append((corner1, corner2))
    return boxes

def slice_images(from_path, to_path, regions):
    for image_index, image_path in enumerate(os.listdir(from_path)):
        full_path = os.path.join(SEPARATED, image_path)
        img = cv2.imread(full_path)
        for index, region in enumerate(regions):
            corner1 = region[0]
            corner2 = region[1]
            crop = img[corner1[0]:corner2[0], corner1[1]:corner2[1]]
            cv2.imwrite(os.path.join(to_path, f'viktorV2_image{image_index}_region{index}.jpg'), crop)

def darken_images(from_path, to_path, regions):
    for image_index, image_path in enumerate(os.listdir(from_path)):
        full_path = os.path.join(SEPARATED, image_path)
        img = cv2.imread(full_path)
        for index, region in enumerate(regions):
            corner1 = region[0]
            corner2 = region[1]
            black_img = np.zeros([IMAGE_SIZE[0], IMAGE_SIZE[1], 3], dtype=np.uint8)
            black_img[corner1[0]:corner2[0], corner1[1]:corner2[1]] = img[corner1[0]:corner2[0], corner1[1]:corner2[1]]
            cv2.imwrite(os.path.join(to_path, f'viktorV2_image{image_index}_region{index}.jpg'), black_img)



regions = read_regions(REGIONS)
slice_images(SEPARATED, SLICED, regions)
darken_images(SEPARATED, DARKENED, regions)


