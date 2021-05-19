import os
import sys

from ed_adapters.ed_adapter_default import EDAdapterDefault
from entities.event_detector import EventDetector
from entities.microscope_manual import MicroscopeManual
from entities.user_settings import UserSettings
from logs.log_setup import setup_loggers
from am_adapters.am_adapter_avi import AMAdapterAVI
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
    """
    :param func: a function that we want to apply.
    :return: a function that executes the above function in the case that the system has not executed.
    """
    def wrap(self, *args, **kwargs):
        if self.executing:
            self.publisher.publish(Events.executing_event, 'Program already running')
        else:
            return func(self, *args, **kwargs)
    return wrap


def check_if_parameters_set(func):
    """
    :param func: a function that we want to apply.
    :return: a function that executes the above function in the case that the required parameters for execution are all
    set.
    """
    def wrap(self, *args, **kwargs):
        detector = self.chosen_detector
        path = self.working_dir
        user_settings = self.user_settings
        if detector is None or path is None or user_settings is None:
            print("Parameters are not set")
        else:
            return func(self, *args, **kwargs)
    return wrap


class Controller:
    """
    This class is responsible to the communicate between the different components of the system.
    """
    def __init__(self):
        self.executing = False          # a boolean field that indicates whether the microscope is under execution.
        self.am_adapter = None          # the am_adapter of the system.
        self.ed_adapter = None          # the ed_adapter of the system.
        self.problem_domain = None      # the problem domain for the next execution.
        self.microscope = None          # the microscope for the next execution.
        self.working_dir = None         # the working directory next execution.
        self.user_settings = None       # the settings that the user has fed to the microscope for the next execution.
        self.detectors_path = None      # the path of the event detector that is chosen for the next execution.
        self.detectors = []             # the event detectors that are available
        self.publisher = Publisher()    # the controller's publisher
        self.chosen_detector = None     # the detector that has been chosen to the next execution.

        self.problem_domains = ["Cell Fusion - Fly Spit"]
        self.domain_microscopes = {"Cell Fusion - Fly Spit": ["AVI"]}
        self.microscopes = {("Cell Fusion - Fly Spit", "AVI"): MicroscopeManual(AVI_SETTINGS)}

    @check_if_running
    def get_detectors(self):
        """
        :return: This method adds to the detectors list the detectors which are in the directory with the path
        detectors_path.
        """
        if not self.detectors:
            for name in os.listdir(self.detectors_path):
                if os.path.isdir(os.path.join(self.detectors_path, name)):
                    self.detectors.append(EventDetector(os.path.join(self.detectors_path, name)))
        return self.detectors

    @check_if_running
    def set_problem_domain(self, index):
        """
        :param index: the index of the problem domain in the list of the problem domains.
        :return: the list of the microscopes that can are responsible to the specified problem domain.
        """
        self.problem_domain = self.problem_domains[index]
        return self.domain_microscopes[self.problem_domain]

    @check_if_running
    def set_microscope(self, index):
        """
        :param index: the index of the microscope in the list of the microscopes.
        This method sets the chosen microscope to be the microscope of the controller in the next execution.
        """
        self.microscope = self.domain_microscopes[self.problem_domain][index]

    @check_if_running
    def set_detector(self, index):
        """
        :param index: the index of the detector in the list of the detectors.
        This method sets the chosen detector to be the detector of the controller in the next execution.
        """
        self.chosen_detector = self.detectors[index]

    @check_if_running
    def set_working_dir(self, path):
        """
        :param path: a path to working directory.
        This method sets the path of the working directory for the next execution.
        """
        self.working_dir = path

    @check_if_running
    def set_detectors_path(self, path):
        """
        :param path: a path to detectors directory.
        This method sets the controller's path of the detectors directory.
        """
        self.detectors_path = path

    @check_if_parameters_set
    @check_if_running
    def run(self):
        """
        This method start the execution of the adapters.
        """
        self.executing = True
        self.am_adapter = AMAdapterAVI(self.user_settings, self.working_dir)
        self.ed_adapter = EDAdapterDefault(self.chosen_detector, self.working_dir)

        # delete images from working dir
        for file in os.listdir(self.ed_adapter.image_path):
            os.remove(os.path.join(self.ed_adapter.image_path, file))

        t = Thread(target=self.ed_adapter.adapter_loop)

        self.am_adapter.activate_microscope()
        self.ed_adapter.publisher.subscribe(Events.model_detection_event)(self.forward_model_detection)
        self.ed_adapter.publisher.subscribe(Events.image_event)(self.forward_image)

        t.start()

    def forward_image(self, image):
        """
        :param image: an image that the controller has accepted.
        This method publishes an image event for the controller's publisher with the image parameter.
        """
        self.publisher.publish(Events.image_event, image)

    def forward_model_detection(self, coords=None):
        """
        :param coords: the coordinates of the detection of an event that occurred.
        This method publishes a model detection event for the am_adapters's publisher with the coords parameter.
        """
        self.am_adapter.event_handle(coords)

    @check_if_running
    def apply_settings(self, values):
        """
        :param values: the values of the user settings to send to the microscope.
        This method set the user_settings member of the controller to have the values from above.
        """
        settings = {}
        for key, value in zip(self.microscopes[(self.problem_domain, self.microscope)].settings_keys, values):
            settings[key] = value
        self.user_settings = UserSettings(settings)

    def get_event_detector(self):
        """
        :return: this method returns the chosen event detector of the controller.
        """
        return self.chosen_detector

    def get_user_settings(self):
        """
        :return: this method returns the user settings of the controller.
        """
        return self.user_settings.settings_map

    def stop(self):
        """
        This method stop the execution of the adapters.
        """
        if self.executing is True:
            if self.ed_adapter is not None:
                self.ed_adapter.stop()
            self.executing = False
            print('Execution is stopped')
        else:
            print('System is not being executed')
