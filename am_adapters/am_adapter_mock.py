from am_adapters.am_adapter_abc import AMAdapter
from definitions import global_vars, VARNAMES, ROOT_DIR
import os
import time
import tifffile as tiff
from subprocess import Popen




class AMAdapterMock(AMAdapter):
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

    def read_actions_config(self):
        f = open(global_vars[VARNAMES.actions_file_path.value], 'r')
        text = f.read()
        f.close()
        return text

    def translate_actions(self, actions, coords):
        ans = []
        for (x, y) in coords:
            for act in actions.split('\n'):
                if act == 'move':
                    ans.append(f'move {x},{y}')
                if act == 'burn':
                    ans.append('burn')
                if 'zoom' in act:
                    ans.append(act)
        return '\n'.join(ans)

    def activate_microscope(self, actions):
        f = open(global_vars[VARNAMES.translated_actions_file_path.value], 'w')
        f.write(actions)
        f.close()
        Popen(f'python {os.path.join(ROOT_DIR, "microscope_action_mock.py")} {global_vars[VARNAMES.translated_actions_file_path.value]}')

