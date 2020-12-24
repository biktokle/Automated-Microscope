from ed_adapters.ed_adapter_abc import EDAdapter
from definitions import global_vars, VARNAMES
import os
import tifffile as tiff
from subprocess import Popen




class EDAdapterMock(EDAdapter):

    def consume_image(self):
        files = []
        while not files:
            try:
                files = os.listdir(global_vars[VARNAMES.image_path.value])
            except FileNotFoundError as no_such_dir:
                raise Exception(f'Image directory does not exist: {no_such_dir}')
            except Exception as e:
                raise Exception(f'Image directory was not set up: {e}')
        if len(files) > 1:
            raise Exception('More than one image in directory, ambiguous')
        full_path = os.path.join(global_vars[VARNAMES.image_path.value], files[0])
        image = tiff.imread(full_path)
        os.remove(full_path)
        return image

    def process_image(self, im):
        tiff.imsave(global_vars[VARNAMES.processed_image_path.value], im)

    def feed_to_event_detector(self, processed_im):
        Popen(f'python {global_vars[VARNAMES.ed_path.value]} {global_vars[VARNAMES.processed_image_path.value]} {global_vars[VARNAMES.coordinates_file_path.value]}')
