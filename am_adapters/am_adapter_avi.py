from am_adapters.am_adapter_abc import AMAdapter
import os
import json

CONFIG_FILE = 'config.json'
EVENT_FILE = 'ed_output.json'


class AMAdapterAVI(AMAdapter):
    """
    This class is responsible for the communication with the AVI microscope.
    """
    def __init__(self, user_settings, working_dir):
        self.user_settings = user_settings
        self.working_dir = working_dir
        self.user_settings_path = os.path.join(self.working_dir, CONFIG_FILE)   # the path to the user settings file
        self.ed_output_path = os.path.join(self.working_dir, EVENT_FILE)        # the path to the event detection file

    def activate_microscope(self):
        with open(self.user_settings_path, 'w+') as file:
            file.write(json.dumps(self.user_settings.settings_map))
            file.close()

    def parse_regions(self):
        pass

    def event_handle(self, coords):
        with open(self.ed_output_path, 'w+') as file:
            detection = dict()
            if coords is None:
                detection['event_detected'] = False
                file.write(json.dumps(detection))
            else:
                detection['event_detected'] = True
                detection['event_rect_x'] = [coords['xmin'], coords['xmax']]
                detection['event_rect_y'] = [coords['ymin'], coords['ymax']]
                file.write(json.dumps(detection))
