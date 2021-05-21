import unittest
from unittest import TestCase
from unittest.mock import MagicMock

from controller.controller import Controller
import os
from pathlib import Path
from entities.event_detector import EventDetector
from entities.user_settings import UserSettings
from ed_adapters.ed_adapter_default import IMAGES_PATH

dirpath = os.path.dirname(__file__)
DETECTOR_PATH = os.path.join(dirpath, '../test_resources/mock_detectors')
WORK_DIR = os.path.join(dirpath, '../test_resources/tests_workdir')


class TestController(TestCase):

    def setUp(self):
        self.controller = Controller()
        adapter_mock = MagicMock()
        adapter_mock.get_image_path = MagicMock(return_value=os.path.join(WORK_DIR, IMAGES_PATH))
        self.controller.create_adapters = MagicMock(return_value=(adapter_mock, adapter_mock))

    def test_get_detectors(self):
        detectors_path = os.path.join(Path(__file__).parent.parent.parent.parent, 'event_detectors')
        self.controller.set_detectors_path(detectors_path)
        controller_detectors = [detector.name for detector in self.controller.get_detectors()]

        detectors = os.listdir(detectors_path)

        assert controller_detectors == detectors

    def test_get_detectors_running(self):
        execute(self.controller)
        detectors = self.controller.get_detectors()

        cond1 = detectors is None
        self.controller.stop()

        detectors = self.controller.get_detectors()
        cond2 = detectors is not None

        assert cond1 and cond2

    def test_set_problem_domain(self):
        self.controller.set_problem_domain(0)
        assert self.controller.problem_domain == self.controller.problem_domains[0]

    def test_set_problem_domain_running(self):
        execute(self.controller)
        problem_domain = self.controller.problem_domain

        self.controller.set_problem_domain(0)
        cond1 = self.controller.problem_domain == problem_domain

        self.controller.stop()
        self.controller.set_problem_domain(0)
        cond2 = self.controller.problem_domain == self.controller.problem_domains[0]

        assert cond1 and cond2

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()


def execute(controller):
    controller.chosen_detector = EventDetector(os.path.join(DETECTOR_PATH, 'mock_detector'))
    controller.working_dir = WORK_DIR
    controller.user_settings = UserSettings({'test': 'test'})
    controller.run()
