
import os
import sys
from entities.event_detector import EventDetector
from entities.microscope_manual import MicroscopeManual
from logs.log_setup import setup_loggers
from ed_adapters.ed_adapter_mock import EDAdapterMock
from am_adapters.am_adapter_mock import AMAdapterMock
from definitions import global_vars, VARNAMES
import logging
from threading import Thread

parent_dir = os.path.split(os.getcwd())[0]
sys.path.extend([x[0] for x in os.walk(parent_dir) if '.git' not in x[0]])

executing = False

setup_loggers()
info_logger = logging.getLogger('info')
error_logger = logging.getLogger('exceptions')

MOCK_MAPPING = {"burn": "burn", "zoom in": "zoom in", "zoom out": "zoom out",
                "position": "position", "report": "report"}


def check_if_running(func):
    def wrap(*args, **kwargs):
        if executing:
            print("bla bla")
        else:
            return func(*args, **kwargs)
    return wrap


class Controller:
    def __init__(self):
        self.am_adapter = None
        self.ed_adapter = None
        self.problem_domain = None
        self.microscope = None
        self.image_path = None
        self.action_config = None
        self.problem_domains = ["Cell Fusion - Fly Spit"]
        self.domain_microscopes = {"Cell Fusion - Fly Spit": ["MOCK"]}
        self.microscopes = {"MOCK": MicroscopeManual(MOCK_MAPPING)}
        self.detectors = []
        self.chosen_detector = None

    @check_if_running
    def get_detectors(self):
        if not self.detectors:
            for name in os.listdir(global_vars[VARNAMES.ed_path.value]):
                if os.path.isdir(os.path.join(global_vars[VARNAMES.ed_path.value], name)):
                    self.detectors.append(EventDetector(os.path.join(global_vars[VARNAMES.ed_path.value], name)))
        return self.detectors

    @check_if_running
    def set_problem_domain(self, index):
        self.problem_domain = self.problem_domains[index]
        return self.domain_microscopes[self.problem_domain]

    @check_if_running
    def set_microscope(self, index):
        self.microscope = self.domain_microscopes[self.problem_domain][index]

    @check_if_running
    def set_detector(self, index):
        self.chosen_detector = self.detectors[index]

    @check_if_running
    def set_image_path(self, path):
        self.image_path = path

    @check_if_running
    def run(self):
        self.check_if_parameters_set()
        global executing
        executing = True
        self.am_adapter = AMAdapterMock(self.action_config)
        self.ed_adapter = EDAdapterMock(self.chosen_detector.detector_path, self.image_path)
        t1 = Thread(target=self.am_adapter.adapter_loop)
        t2 = Thread(target=self.ed_adapter.adapter_loop)

        t1.start()
        t2.start()

    @check_if_running
    def apply_configuration(self, configuration):
        self.action_config = configuration


    def check_if_parameters_set(self):
        if self.chosen_detector is None or self.image_path is None or self.action_config is None:
            raise Exception("Parameters are not set")

    def get_event_detector(self):
        return self.chosen_detector

    def get_action_configuration(self):
        return self.action_config

    def stop(self):
        if self.am_adapter is not None:
            self.am_adapter.stop()
        if self.ed_adapter is not None:
            self.ed_adapter.stop()
        exit(1)
