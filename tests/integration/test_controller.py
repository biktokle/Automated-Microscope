import unittest
from unittest import TestCase
from controller.controller import Controller
import os
from pathlib import Path
from threading import Thread


class TestController(TestCase):

    def setUp(self):
        self.controller = Controller()

    def test_get_detectors(self):
        detectors_path = os.path.join(Path(__file__).parent.parent.parent.parent, 'event_detectors')
        self.controller.set_detectors_path(detectors_path)
        controller_detectors = [detector.name for detector in self.controller.get_detectors()]

        detectors = os.listdir(detectors_path)

        assert controller_detectors == detectors

    def test_get_detectors_running(self):
        execute(self.controller)
        self.controller.get_detectors()
        self.controller.stop()

    def tearDown(self):
        print('Hello')


if __name__ == '__main__':
    unittest.main()


def execute(controller):
    root_dir = Path(__file__).parent.parent.parent.parent
    detectors_path = os.path.join(root_dir, 'event_detectors')
    working_dir = os.path.join(root_dir, 'working_dir')
    controller.set_working_dir(working_dir)
    controller.set_problem_domain(0)
    controller.set_microscope(0)
    controller.set_detectors_path(detectors_path)
    controller.get_detectors()
    controller.set_detector()
    controller.apply_settings([1, 1, 1, 1, 1])
    controller.run()
