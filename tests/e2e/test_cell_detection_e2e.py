import json
import unittest
from time import sleep
from unittest import TestCase

from controller.controller import Controller
from entities.event_detector import EventDetector
import os
import shutil

from entities.user_settings import UserSettings

dirpath = os.path.dirname(__file__)
DETECTOR_PATH = os.path.join(dirpath, '../test_resources/mock_detectors')
WORK_DIR = os.path.join(dirpath, '../test_resources/tests_workdir')
IMAGE_DIR = os.path.join(dirpath, '../test_resources/test_images')

ED_OUTPUT = 'ed_output.json'
CONFIG = 'config.json'

class E2ETests(TestCase):

    def setUp(self):
        self.controller = Controller()
        self.controller.chosen_detector = EventDetector(os.path.join(DETECTOR_PATH, 'mock_detector'))
        self.controller.working_dir = WORK_DIR
        self.controller.user_settings = UserSettings({'test': 'test'})

    def test_e2e(self):
        """
        This test creates 4 images and uses a mock detector to test the flow of the system.
        3 times there is no event, in the 4th time there is a detected event.
        """
        self.controller.run()
        with open(os.path.join(WORK_DIR, CONFIG)) as f:
            assert json.loads(f.read())['test'] == 'test'
        os.remove(os.path.join(WORK_DIR, CONFIG))
        for i in range(3):
            shutil.copyfile(os.path.join(IMAGE_DIR, '0.tif'), os.path.join(WORK_DIR, 'images', '0.tif'))
            self.__assert_no_event()

        shutil.copyfile(os.path.join(IMAGE_DIR, '0.tif'), os.path.join(WORK_DIR, 'images', '0.tif'))
        self.__assert_event()
        self.controller.stop()

    def __assert_no_event(self):
        while not os.path.exists(os.path.join(WORK_DIR, ED_OUTPUT)):
            continue
        sleep(0.1)
        with open(os.path.join(WORK_DIR, ED_OUTPUT)) as f:
            assert not json.loads(f.read())['event_detected']
        os.remove(os.path.join(WORK_DIR, ED_OUTPUT))

    def __assert_event(self):
        while not os.path.exists(os.path.join(WORK_DIR, ED_OUTPUT)):
            continue
        sleep(0.1)
        with open(os.path.join(WORK_DIR, ED_OUTPUT)) as f:
            event = json.loads(f.read())
            assert event['event_detected'] and event['event_rect_x'] == [200, 220] \
                   and event['event_rect_y'] == [200, 220]
        os.remove(os.path.join(WORK_DIR, ED_OUTPUT))


if __name__ == '__main__':
    unittest.main()
