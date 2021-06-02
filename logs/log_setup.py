import logging
import os


LOGGER_DIR = os.path.dirname(os.path.abspath(__file__))


def setup_loggers():
    l = logging.getLogger('exceptions')
    fileHandler = logging.FileHandler(os.path.join(LOGGER_DIR, 'errors.log'), mode='w+')
    fileHandler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    l.setLevel(logging.DEBUG)
    l.addHandler(fileHandler)

    l1 = logging.getLogger('info')
    fileHandler1 = logging.FileHandler(os.path.join(LOGGER_DIR, 'info.log'), mode='w+')
    fileHandler1.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    l1.setLevel(logging.DEBUG)
    l1.addHandler(fileHandler1)
