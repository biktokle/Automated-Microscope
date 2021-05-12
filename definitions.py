import os
from enum import Enum

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGER_DIR = os.path.join(ROOT_DIR, 'logs')
WORKING_DIR = r'C:\Users\viktor_koukouliev\Desktop\WORKDIR'
global_vars = {}
# global_vars['image_path'] = r'C:\Users\vkoukoul\PycharmProjects\Automated-Microscope\microscope_output\\'
# global_vars['processed_image_path'] = r'C:\Users\vkoukoul\PycharmProjects\Automated-Microscope\processed_images\\example.tif'
# global_vars['ed_path'] = r'C:\Users\vkoukoul\PycharmProjects\Automated-Microscope\detectors\\mock_detector.py'
# global_vars['coordinates_file_path'] = r'C:\Users\vkoukoul\PycharmProjects\Automated-Microscope\coordinates\\cords.txt'
# global_vars['actions_file_path'] = r'C:\Users\vkoukoul\PycharmProjects\Automated-Microscope\actions_config\\actions.txt'
# global_vars['translated_actions_file_path'] = r'C:\Users\vkoukoul\PycharmProjects\Automated-Microscope\translated_actions\\actions.txt'

global_vars['image_path'] = os.path.join(WORKING_DIR, r'microscope_output')
global_vars['roi'] = os.path.join(WORKING_DIR, r'regions_of_interest.txt')
global_vars['processed_image_path'] = os.path.join(ROOT_DIR, r'processed_images', r'example.jpg')
global_vars['ed_path'] = os.path.join(ROOT_DIR, r'detectors')
global_vars['coordinates_file_path'] = os.path.join(ROOT_DIR, r'coordinates', r'cords.txt')
global_vars['actions_file_path'] = os.path.join(ROOT_DIR, r'actions_config', r'actions.txt')
global_vars['translated_actions_file_path'] = os.path.join(ROOT_DIR, r'translated_actions', r'actions.txt')


class VARNAMES(Enum):
    image_path = 'image_path'
    processed_image_path = 'processed_image_path'
    coordinates_file_path = 'coordinates_file_path'
    actions_file_path = 'actions_file_path'
    translated_actions_file_path = 'translated_actions_file_path'
    ed_path = 'ed_path'
    info_logger = 'info_logger'
    error_logger = 'error_logger'
    roi = 'roi'

