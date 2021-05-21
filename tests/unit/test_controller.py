import os
import unittest
from unittest import TestCase
from unittest.mock import MagicMock
from pathlib import Path

from controller.controller import Controller
from entities.microscope_manual import MicroscopeManual
from notification.publisher import Events

dirpath = os.path.dirname(__file__)
DETECTOR_PATH = os.path.join(dirpath, '../test_resources/mock_detectors')
WORK_DIR = os.path.join(dirpath, '../test_resources/tests_workdir')
MOCK_SETTINGS = ['settings1', 'settings2', 'settings3', 'settings4']
MOCK_PROBLEM = 'Mock_Problem'


class TestController(TestCase):

    def setUp(self):
        self.controller = Controller()
        self.controller.create_adapters = MagicMock(return_value=(MagicMock(), MagicMock()))

        self.detectors_path = os.path.join(Path(__file__).parent.parent.parent.parent, 'event_detectors')
        self.controller.set_detectors_path(self.detectors_path)

        self.controller.problem_domains.append(MOCK_PROBLEM)
        self.controller.domain_microscopes[MOCK_PROBLEM] = ['Mock_Microscope']
        self.controller.microscopes[('Mock_Problem', 'Mock_Microscope')] = MicroscopeManual(MOCK_SETTINGS)

    def test_stop_when_running(self):
        self.controller.executing = True
        self.controller.ed_adapter = MagicMock()
        self.controller.ed_adapter.stop = MagicMock()
        self.controller.stop()
        assert self.controller.ed_adapter.stop.called

    def test_stop_when_not_running(self):
        self.controller.ed_adapter = MagicMock()
        self.controller.ed_adapter.stop = MagicMock()
        self.controller.stop()
        assert not self.controller.ed_adapter.stop.called

    def test_check_if_running(self):
        self.controller.executing = True
        method = MagicMock()
        self.controller.publisher.subscribe(Events.executing_event)(method)
        self.controller.get_detectors()
        assert method.called

    def test_get_detectors(self):
        controller_detectors = [detector.name for detector in self.controller.get_detectors()]
        detectors = os.listdir(self.detectors_path)
        assert controller_detectors == detectors

    def test_set_problem_domain(self):
        self.controller.set_problem_domain(0)
        assert self.controller.problem_domain == self.controller.problem_domains[0]

    def test_set_microscope(self):
        problem_domain = self.controller.problem_domains[0]
        self.controller.problem_domain = problem_domain
        self.controller.set_microscope(0)
        assert self.controller.microscope == self.controller.domain_microscopes[problem_domain][0]

    def test_set_detector(self):
        self.controller.set_detector(0)
        assert self.controller.chosen_detector == self.controller.detectors[0]

    def test_set_working_dir(self):
        self.controller.set_working_dir(WORK_DIR)
        assert self.controller.working_dir == WORK_DIR

    def test_set_detectors_path(self):
        detectors_path = os.path.join(Path(__file__).parent.parent.parent.parent, 'event_detectors')
        self.controller.set_detectors_path(detectors_path)
        controller_detectors = [detector.name for detector in self.controller.detectors]

        detectors = os.listdir(detectors_path)
        assert controller_detectors == detectors

    def test_apply_settings(self):
        apply_settings(self.controller)
        user_settings = self.controller.user_settings.settings_map

        cond = True
        for i in range(len(MOCK_SETTINGS)):
            cond = cond and user_settings[MOCK_SETTINGS[i]] == i

        assert cond


if __name__ == '__main__':
    unittest.main()


def apply_settings(controller):
    controller.problem_domain = controller.problem_domains[1]
    controller.microscope = controller.domain_microscopes[MOCK_PROBLEM][0]
    controller.apply_settings(list(range(len(MOCK_SETTINGS))))
