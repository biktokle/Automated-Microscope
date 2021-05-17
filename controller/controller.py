
import os
import sys

from ed_adapters.ed_adapter_default import EDAdapterDefault
from entities.event_detector import EventDetector
from entities.microscope_manual import MicroscopeManual
from entities.user_settings import UserSettings
from logs.log_setup import setup_loggers
from ed_adapters.ed_adapter_mock import EDAdapterMock
from am_adapters.am_adapter_mock import AMAdapterMock
from definitions import global_vars, VARNAMES
import logging
from threading import Thread

from notification.publisher import Publisher, Events

parent_dir = os.path.split(os.getcwd())[0]
sys.path.extend([x[0] for x in os.walk(parent_dir) if '.git' not in x[0]])



setup_loggers()
info_logger = logging.getLogger('info')
error_logger = logging.getLogger('exceptions')

AVI_SETTINGS = ['intervals', 't_points', 'channel', 'exposure', 'laser_power']


def check_if_running(func):
    def wrap(self, *args, **kwargs):
        if self.executing:
            self.publisher.publish(Events.executing_event, 'Program already running')
        else:
            return func(self, *args, **kwargs)
    return wrap


def check_if_parameters_set(func):
    def wrap(self, *args, **kwargs):
        detector = self.chosen_detector
        path = self.image_path
        user_settings = self.user_settings
        if detector is None or path is None or user_settings is None:
            print("Parameters are not set")
        else:
            return func(self, *args, **kwargs)
    return wrap


class Controller:
    def __init__(self):
        self.executing = False
        self.am_adapter = None
        self.ed_adapter = None
        self.problem_domain = None
        self.microscope = None
        self.image_path = None
        self.user_settings = None
        self.detectors_path = None
        self.problem_domains = ["Cell Fusion - Fly Spit"]
        self.domain_microscopes = {"Cell Fusion - Fly Spit": ["AVI"]}
        self.microscopes = {("Cell Fusion - Fly Spit", "AVI"): MicroscopeManual(AVI_SETTINGS)}
        self.detectors = []
        self.publisher = Publisher()
        self.chosen_detector = None

    @check_if_running
    def get_detectors(self):
        if not self.detectors:
            for name in os.listdir(self.detectors_path):
                if os.path.isdir(os.path.join(self.detectors_path, name)):
                    self.detectors.append(EventDetector(os.path.join(self.detectors_path, name)))
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
    def set_detectors_path(self, path):
        self.detectors_path = path

    @check_if_parameters_set
    @check_if_running
    def run(self):
        # delete images from working dir
        for file in os.listdir(self.image_path):
            os.remove(os.path.join(self.image_path, file))
        self.executing = True
        self.am_adapter = AMAdapterMock(self.user_settings, self.microscopes[(self.problem_domain, self.microscope)])
        self.ed_adapter = EDAdapterDefault(self.chosen_detector, self.image_path)
        t1 = Thread(target=self.am_adapter.adapter_loop)
        t2 = Thread(target=self.ed_adapter.adapter_loop)

        self.publisher.subscribe(Events.model_detection_event)(self.forward_model_detection)
        self.ed_adapter.publisher.subscribe(Events.image_event)(self.forward_image)

        t1.start()
        t2.start()

    def forward_image(self, image):
        self.publisher.publish(Events.image_event, image)

    def forward_model_detection(self, coords):
        self.am_adapter.publisher.publish(Events.model_detection_event, coords)

    @check_if_running
    def apply_settings(self, values):
        settings = {}
        for key, value in zip(self.microscopes[(self.problem_domain, self.microscope)].settings_keys, values):
            settings[key] = value
        self.user_settings = UserSettings(settings)

    def get_event_detector(self):
        return self.chosen_detector

    def get_user_settings(self):
        return self.user_settings.settings_map

    def stop(self):
        if self.executing is True:
            if self.am_adapter is not None:
                self.am_adapter.stop()
            if self.ed_adapter is not None:
                self.ed_adapter.stop()
            self.executing = False
            print('Execution is stopped')
        else:
            print('System is not being executed')

