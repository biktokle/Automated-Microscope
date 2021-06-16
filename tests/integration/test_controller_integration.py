import unittest
from unittest import TestCase
from unittest.mock import MagicMock

from controller.controller import Controller
import os
from pathlib import Path
from entities.event_detector import EventDetector
from entities.microscope_manual import MicroscopeManual
from entities.user_settings import UserSettings
from ed_adapters.ed_adapter_default import IMAGES_PATH

dirpath = os.path.dirname(__file__)
DETECTOR_PATH = os.path.join(dirpath, '../test_resources/mock_detectors')
WORK_DIR = os.path.join(dirpath, '../test_resources/tests_workdir')
MOCK_DIR = 'Just/A/Mock/Directory'
MOCK_SETTINGS = ['settings1', 'settings2', 'settings3', 'settings4']
MOCK_PROBLEM = 'Mock_Problem'
SOFTWARE_CONFIG_PATH = os.path.join(dirpath, '../test_resources/software_config.json')

class TestController(TestCase):

    def setUp(self):
        self.controller = Controller(SOFTWARE_CONFIG_PATH)
        adapter_mock = MagicMock()
        adapter_mock.get_image_path = MagicMock(return_value=os.path.join(WORK_DIR, IMAGES_PATH))
        self.controller.create_adapters = MagicMock(return_value=(adapter_mock, adapter_mock))

        self.controller.set_detectors_path(DETECTOR_PATH)

        self.controller.problem_domains.append(MOCK_PROBLEM)
        self.controller.domain_microscopes[MOCK_PROBLEM] = ['Mock_Microscope1', 'Mock_Microscope2']
        self.controller.microscopes[('Mock_Problem', 'Mock_Microscope1')] = MicroscopeManual(MOCK_SETTINGS)
        self.controller.microscopes[('Mock_Problem', 'Mock_Microscope2')] = MicroscopeManual(MOCK_SETTINGS)

    def test_get_detectors(self):
        detectors = os.listdir(DETECTOR_PATH)

        controller_detectors = [detector.name for detector in self.controller.get_detectors()]
        cond1 = controller_detectors == detectors

        execute(self.controller)
        controller_detectors = self.controller.get_detectors()
        cond2 = controller_detectors is None

        self.controller.stop()
        controller_detectors = [detector.name for detector in self.controller.get_detectors()]
        cond3 = detectors == controller_detectors

        assert cond1 and cond2 and cond3

    def test_set_problem_domain(self):
        self.controller.set_problem_domain(0)
        cond1 = self.controller.problem_domain == self.controller.problem_domains[0]

        execute(self.controller)
        problem_domain = self.controller.problem_domain

        self.controller.set_problem_domain(1)
        cond2 = self.controller.problem_domain == problem_domain

        self.controller.stop()
        self.controller.set_problem_domain(1)
        cond3 = self.controller.problem_domain == self.controller.problem_domains[1]

        assert cond1 and cond2 and cond3

    def test_set_microscope(self):
        problem_domain = self.controller.problem_domains[1]
        self.controller.problem_domain = problem_domain
        self.controller.set_microscope(0)
        cond1 = self.controller.microscope == self.controller.domain_microscopes[problem_domain][0]

        execute(self.controller)
        self.controller.set_microscope(1)
        cond2 = self.controller.microscope == self.controller.domain_microscopes[problem_domain][0]

        self.controller.stop()
        self.controller.set_microscope(1)
        cond3 = self.controller.microscope == self.controller.domain_microscopes[problem_domain][1]

        assert cond1 and cond2 and cond3

    def test_set_detector(self):
        self.controller.set_detectors_path(DETECTOR_PATH)

        self.controller.set_detector(0)
        cond1 = self.controller.chosen_detector == self.controller.detectors[0]

        execute(self.controller)
        self.controller.set_detector(1)

        cond2 = self.controller.chosen_detector != self.controller.detectors[1]

        self.controller.stop()
        self.controller.set_detector(1)

        cond3 = self.controller.chosen_detector == self.controller.detectors[1]
        assert cond1 and cond2 and cond3

    def test_working_dir(self):
        self.controller.set_detectors_path(DETECTOR_PATH)
        cond1 = self.controller.detectors_path == DETECTOR_PATH

        execute(self.controller)
        self.controller.set_working_dir(MOCK_DIR)

        cond2 = self.controller.working_dir == WORK_DIR

        self.controller.stop()

        assert cond1 and cond2

    def test_set_detectors_path(self):
        controller_detectors = [detector.name for detector in self.controller.detectors]
        detectors = os.listdir(DETECTOR_PATH)
        cond1 = controller_detectors == detectors

        execute(self.controller)
        self.controller.set_detectors_path(MOCK_DIR)
        cond2 = controller_detectors == detectors

        self.controller.stop()
        self.controller.set_detectors_path(WORK_DIR)
        detectors = os.listdir(DETECTOR_PATH)
        controller_detectors = [detector.name for detector in self.controller.detectors]
        cond3 = detectors != controller_detectors

        assert cond1 and cond2 and cond3

    def test_apply_settings(self):
        self.controller.problem_domain = self.controller.problem_domains[1]
        self.controller.microscope = self.controller.domain_microscopes[MOCK_PROBLEM][0]
        self.controller.apply_settings(list(range(len(MOCK_SETTINGS))))
        user_settings = self.controller.user_settings.settings_map

        cond = True
        for i in range(len(MOCK_SETTINGS)):
            cond = cond and user_settings[MOCK_SETTINGS[i]] == i

        execute(self.controller)
        user_settings = self.controller.user_settings.settings_map
        self.controller.apply_settings(list(range(5, 5 + len(MOCK_SETTINGS))))
        cond = cond and user_settings == self.controller.user_settings.settings_map

        self.controller.stop()
        self.controller.apply_settings(list(range(5, len(MOCK_SETTINGS) + 5)))
        user_settings = self.controller.user_settings.settings_map

        for i in range(len(MOCK_SETTINGS)):
            cond = cond and user_settings[MOCK_SETTINGS[i]] == i + 5

        assert cond


if __name__ == '__main__':
    unittest.main()


def execute(controller):
    controller.chosen_detector = EventDetector(os.path.join(DETECTOR_PATH, 'mock_detector'))
    controller.working_dir = WORK_DIR
    controller.user_settings = UserSettings({'test': 'test'})
    controller.problem_domain = MOCK_PROBLEM
    controller.microscope = controller.domain_microscopes[MOCK_PROBLEM][0]
    controller.run()
