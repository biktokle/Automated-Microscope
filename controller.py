
import os
import sys
import pathlib



parent_dir = os.path.split(os.getcwd())[0]
sys.path.extend([x[0] for x in os.walk(parent_dir) if '.git' not in x[0]])

from entities.event_detector import EventDetector
from logs.log_setup import setup_loggers
from ed_adapters.ed_adapter_mock import EDAdapterMock
from am_adapters.am_adapter_mock import AMAdapterMock
from definitions import global_vars, VARNAMES
import logging
from threading import Thread

executing = False


setup_loggers()
info_logger = logging.getLogger('info')
error_logger = logging.getLogger('exceptions')






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
        self.detector_path = None
        self.image_path = None
        self.problem_domains = []
        self.detectors = []

    @check_if_running
    def get_detectors(self):
        if not self.detectors:
            for name in os.listdir(global_vars[VARNAMES.ed_path.value]):
                if os.path.isdir(os.path.join(global_vars[VARNAMES.ed_path.value], name)):
                    self.detectors.append(EventDetector(os.path.join(global_vars[VARNAMES.ed_path.value], name)))
        return self.detectors

    @check_if_running
    def set_detector(self, index):
        self.detector_path = self.detectors[index].detector_path

    @check_if_running
    def set_image_path(self, path):
        self.image_path = path

    @check_if_running
    def run(self):
        global executing
        executing = True
        self.am_adapter = AMAdapterMock()
        self.ed_adapter = EDAdapterMock(self.detector_path, self.image_path)
        t1 = Thread(target=self.am_adapter.adapter_loop)
        t2 = Thread(target=self.ed_adapter.adapter_loop)

        t1.start()
        t2.start()

    def stop(self):
        self.am_adapter.stop()
        self.ed_adapter.stop()



