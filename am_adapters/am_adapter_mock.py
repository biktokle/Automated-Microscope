from am_adapters.am_adapter_abc import AMAdapter
from definitions import global_vars, VARNAMES, ROOT_DIR
import os
from subprocess import Popen


class AMAdapterMock(AMAdapter):
    """
    This class is a mock version of the AMAdapter.
    """
    def __init__(self, user_settings, microscope_manual):
        super().__init__(user_settings, microscope_manual)

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

    # def read_actions_config(self):
    #     f = open(global_vars[VARNAMES.actions_file_path.value], 'r')
    #     text = f.read()
    #     f.close()
    #     return text
    #
    # def translate_actions(self, actions, coords):
    #     ans = []
    #     for (x, y) in coords:
    #         for act in actions.split('\n'):
    #             if act == '':
    #                 continue
    #             if act == 'move':
    #                 ans.append(f'move {x},{y}')
    #             else:
    #                 ans.append(self.microscope_manual.actions_mappings[act])
    #     return '\n'.join(ans)

    def activate_microscope(self, coords):
        f = open(global_vars[VARNAMES.translated_actions_file_path.value], 'w')
        f.write(coords)
        f.close()
        Popen(f'python {os.path.join(ROOT_DIR, "microscope_action_mock.py")} {global_vars[VARNAMES.translated_actions_file_path.value]}')

