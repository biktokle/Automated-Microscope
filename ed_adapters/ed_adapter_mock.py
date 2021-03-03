import imageio
from skimage import io

from ed_adapters.ed_adapter_abc import EDAdapter
from definitions import global_vars, VARNAMES
import os
import tifffile as tiff
from subprocess import Popen

from notification.publisher import Events


class EDAdapterMock(EDAdapter):

    def __init__(self, ed_path, image_path):
        super().__init__(ed_path, image_path)

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

        # files = []
        # while not files:
        #     try:
        #         files = os.listdir(global_vars[VARNAMES.image_path.value])
        #     except FileNotFoundError as no_such_dir:
        #         raise Exception(f'Image directory does not exist: {no_such_dir}')
        #     except Exception as e:
        #         raise Exception(f'Image directory was not set up: {e}')
        # if len(files) > 1:
        #     raise Exception('More than one image in directory, ambiguous')
        full_path = os.path.join(self.image_path, files[0])
        print(full_path)
        image = io.imread(full_path)
        os.remove(full_path)
        return image

    def process_image(self, im):
        self.publisher.publish(Events.image_event, im)
        io.imsave(global_vars[VARNAMES.processed_image_path.value], im)

    def feed_to_event_detector(self, processed_im):
        Popen(f'python {self.ed_path} {global_vars[VARNAMES.processed_image_path.value]} {global_vars[VARNAMES.coordinates_file_path.value]}')
