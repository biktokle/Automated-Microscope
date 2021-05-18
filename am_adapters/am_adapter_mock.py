from am_adapters.am_adapter_abc import AMAdapter
from definitions import global_vars, VARNAMES, ROOT_DIR
import os
from subprocess import Popen


class AMAdapterMock(AMAdapter):
    """
    This class is a mock version of the AMAdapter.
    """
    def __init__(self, user_settings):
        super().__init__(user_settings)

    def consume_coords(self):
        if not os.path.exists(global_vars[VARNAMES.coordinates_file_path.value]):
            return None
        f = open(global_vars[VARNAMES.coordinates_file_path.value], 'r')
        text = f.read()
        f.close()
        coords = []
        for x in text.split('\n'):
            if x == '':
                continue
            nums = x.split(',')
            coords.append((nums[0], nums[1]))
        os.remove(global_vars[VARNAMES.coordinates_file_path.value])
        return coords

    def activate_microscope(self, coords):
        f = open(global_vars[VARNAMES.translated_actions_file_path.value], 'w')
        f.write(coords)
        f.close()
        Popen(f'python {os.path.join(ROOT_DIR, "microscope_action_mock.py")} {global_vars[VARNAMES.translated_actions_file_path.value]}')

