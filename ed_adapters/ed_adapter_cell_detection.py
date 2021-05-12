from time import sleep
import numpy as np
from skimage import io

from definitions import global_vars, VARNAMES
from ed_adapters.ed_adapter_abc import EDAdapter
import os

from notification.publisher import Events


class EDAdapterCellDetection(EDAdapter):

    def __init__(self, detector, image_path):
        super().__init__(detector, image_path)
        self.regions = open(global_vars[VARNAMES.roi.value]).read().split('\n')

    def consume_image(self):
        try:
            files = os.listdir(self.image_path)
        except FileNotFoundError as no_such_dir:
            raise Exception(f'Image directory does not exist: {no_such_dir}')
        except Exception as e:
            raise Exception(f'Image directory was not set up: {e}')
        if len(files) > 1:
            raise Exception('More than one image in directory, ambiguous')
        if not files:
            return None

        full_path = os.path.join(self.image_path, files[0])
        sleep(0.1)
        image = None
        while image is None:
            try:
                image = io.imread(full_path)
            except Exception as e:
                print(e)
                sleep(0.1)
        while os.path.exists(full_path):
            try:
                os.remove(full_path)
            except Exception as e:
                sleep(0.1)
        return image

    def process_image(self, im):
        return image_to_8bit_equalized(im)


    def feed_to_event_detector(self, processed_im):
        xmin, xmax, ymin, ymax = tuple(map(lambda x: int(x), self.regions[0].split(',')))
        region_im = processed_im[ymin:ymax, xmin:xmax]
        img = self.detector.detector.detect(region_im)
        processed_im[ymin:ymax, xmin:xmax] = img
        self.publisher.publish(Events.image_event, processed_im)


def image_to_8bit_equalized(image):
    ratio = np.amax(image) / 256
    img8 = (image / ratio).astype('uint8')

    return img8

