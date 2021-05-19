from time import sleep

from skimage import io
from ed_adapters.ed_adapter_abc import EDAdapter
import os
from subprocess import Popen

from notification.publisher import Events
IMAGES_PATH = 'images'
PROCESS_IMAGES_PATH = 'processed_images'
COORDINATES_PATH = 'coordinates'


class EDAdapterMock(EDAdapter):
    """
    This class is a mock version of the ED Adapter.
    """

    def __init__(self, ed_path, working_dir):
        super().__init__(ed_path, working_dir)
        self.image_path = os.path.join(self.working_dir, IMAGES_PATH)
        self.process_images_path = os.path.join(self.working_dir, PROCESS_IMAGES_PATH)
        self.coordinates_path = os.path.join(self.working_dir, COORDINATES_PATH)

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
                image = io.imread(full_path, plugin='matplotlib')
            except Exception as e:
                sleep(0.1)
        while os.path.exists(full_path):
            try:
                os.remove(full_path)
            except Exception as e:
                sleep(0.1)
        return image

    def process_image(self, im):
        self.publisher.publish(Events.image_event, im)
        io.imsave(self.process_images_path, im)

    def feed_to_event_detector(self, processed_im, full_path):
        Popen(f'python {self.detector.ed_path} {self.process_images_path} {self.coordinates_path}')
