import os
from enum import Enum

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGER_DIR = os.path.join(ROOT_DIR, 'logs')
global_vars = {}
# global_vars['image_path'] = r'C:\Users\vkoukoul\PycharmProjects\Automated-Microscope\microscope_output\\'
# global_vars['processed_image_path'] = r'C:\Users\vkoukoul\PycharmProjects\Automated-Microscope\processed_images\\example.tiff'
# global_vars['ed_path'] = r'C:\Users\vkoukoul\PycharmProjects\Automated-Microscope\detectors\\mock_detector.py'
# global_vars['coordinates_file_path'] = r'C:\Users\vkoukoul\PycharmProjects\Automated-Microscope\coordinates\\cords.txt'
# global_vars['actions_file_path'] = r'C:\Users\vkoukoul\PycharmProjects\Automated-Microscope\actions_config\\actions.txt'
# global_vars['translated_actions_file_path'] = r'C:\Users\vkoukoul\PycharmProjects\Automated-Microscope\translated_actions\\actions.txt'

global_vars['image_path'] = ROOT_DIR + r'\microscope_output\\'
global_vars['processed_image_path'] = ROOT_DIR +  r'\processed_images\\example.tiff'
global_vars['ed_path'] = ROOT_DIR + r'\detectors\\mock_detector.py'
global_vars['coordinates_file_path'] = ROOT_DIR + r'\coordinates\\cords.txt'
global_vars['actions_file_path'] = ROOT_DIR + r'\actions_config\\actions.txt'
global_vars['translated_actions_file_path'] = ROOT_DIR + r'\translated_actions\\actions.txt'


class VARNAMES(Enum):
    image_path = 'image_path'
    processed_image_path = 'processed_image_path'
    coordinates_file_path = 'coordinates_file_path'
    actions_file_path = 'actions_file_path'
    translated_actions_file_path = 'translated_actions_file_path'
    ed_path = 'ed_path'
    info_logger = 'info_logger'
    error_logger = 'error_logger'

