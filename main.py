# import os
# import sys
# parent_dir = os.path.split(os.getcwd())[0]
# sys.path.extend([x[0] for x in os.walk(parent_dir) if '.git' not in x[0]])
#
# from logs.log_setup import setup_loggers
# from ed_adapters.ed_adapter_mock import EDAdapterMock
# from am_adapters.am_adapter_mock import AMAdapterMock
# from definitions import global_vars, VARNAMES
# import logging
# from threading import Thread
#
# setup_loggers()
# info_logger = logging.getLogger('info')
# error_logger = logging.getLogger('exceptions')
#
# am_adapter = AMAdapterMock()
# ed_adapter = EDAdapterMock()
# t1 = Thread(target=am_adapter.adapter_loop)
# t2 = Thread(target=ed_adapter.adapter_loop)
#
# t1.start()
# t2.start()
#
# x = input()
# am_adapter.stop()
# ed_adapter.stop()
from time import sleep

from controller import Controller
c = Controller()
c.set_image_path(r'C:\Users\vkoukoul\PycharmProjects\Automated-Microscope\microscope_output')
x = c.get_detectors()
c.set_detector(0)
c.run()



