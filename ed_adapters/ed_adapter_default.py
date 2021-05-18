from subprocess import Popen, PIPE
from time import sleep

import cv2
import numpy as np
from skimage import io

from communication import client, protocol
from communication.client import Client
from definitions import global_vars, VARNAMES
from ed_adapters.ed_adapter_abc import EDAdapter
import os

from notification.publisher import Events


class EDAdapterDefault(EDAdapter):
    """
    This class is a default implementation of the ED Adapter.
    """
    def __init__(self, detector, image_path):
        super().__init__(detector, image_path)
        self.regions = open(global_vars[VARNAMES.roi.value]).read().split('\n')
        self.client = self.setup_communication()

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
            return None, None

        full_path = os.path.join(self.image_path, files[0])
        sleep(0.1)
        image = None
        while image is None:
            try:
                image = io.imread(full_path)
            except Exception as e:
                print(e)
                sleep(0.1)
        return image, full_path

    def process_image(self, im):
        return image_to_8bit_equalized(im)

    def feed_to_event_detector(self, processed_im, full_path):
        xmin, xmax, ymin, ymax = tuple(map(lambda x: int(x), self.regions[0].split(',')))
        region = {'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax}
        request = protocol.create_detection_request(full_path, region)
        self.client.send_request(request)
        response = self.client.get_response()
        while os.path.exists(full_path):
            try:
                os.remove(full_path)
            except Exception as e:
                sleep(0.1)
        detect_response = protocol.parse_response(response)

        detections = detect_response[0]
        b_boxes = detect_response[1]

        region_im = processed_im[ymin:ymax, xmin:xmax]

        if b_boxes is not None:
            for (objectID, vals) in b_boxes.items():
                # draw both the ID of the object and the centroid of the
                # object on the output frame
                text = "{}".format(objectID)
                cv2.putText(region_im, text, (vals['xcenter'] - 10, vals['ycenter'] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 0, 0), 2)
                cv2.circle(region_im, (vals['xcenter'], vals['ycenter']), 4, (0, 255, 0), -1)
                cv2.rectangle(region_im, (vals['xmin'], vals['ymax']), (vals['xmax'], vals['ymin']), (0, 0, 255), 1)

        processed_im[ymin:ymax, xmin:xmax] = region_im
        self.publisher.publish(Events.image_event, processed_im)

        if detections is not None:
            self.publisher.publish(Events.model_detection_event, detections['coords'])


    def setup_communication(self):
        """
        This method sets up a communication channel with the event detector program.
        """
        free_port = client.get_free_port()
        Popen(f'python {self.detector.detector_path} {client.get_free_port()}')
        return Client(free_port)


def image_to_8bit_equalized(image):
    """
    :param image: a microscope image.
    :return: a preprocessed image after converting it to uint8 type.
    """
    ratio = np.amax(image) / 256
    img8 = (image / ratio).astype('uint8')

    return img8

