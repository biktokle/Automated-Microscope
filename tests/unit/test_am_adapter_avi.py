import json
import unittest
from unittest import TestCase
from am_adapters.am_adapter_avi import AMAdapterAVI, CONFIG_FILE, EVENT_FILE
import os
from entities.user_settings import UserSettings


class TestAMAdapterAVI(TestCase):

    def setUp(self):
        self.settings_map = dict()
        self.settings_map['test_key1'] = 'test_value1'
        self.settings_map['test_key2'] = 'test_value2'
        self.settings_map['test_key3'] = 'test_value3'

        self.coords = dict()
        self.coords['event_rect_x'] = [100, 200]
        self.coords['event_rect_y'] = [300, 400]
        self.coords['event_detected'] = True

        self.working_dir = os.path.dirname(os.path.realpath(__file__))
        self.am_adapter = AMAdapterAVI(UserSettings(self.settings_map), self.working_dir)

    def test_activate_microscope(self):
        self.am_adapter.activate_microscope()

        file_path = os.path.join(self.working_dir, CONFIG_FILE)

        with open(file_path) as file:
            data = json.load(file)

            assert data == self.settings_map

    def test_parse_regions(self):
        assert True

    def test_event_handle_without_coords(self):
        self.am_adapter.event_handle(None)

        file_path = os.path.join(self.working_dir, EVENT_FILE)

        with open(file_path) as file:
            data = json.load(file)

            assert data['event_detected'] is False

    def test_event_handle_with_coords(self):
        self.am_adapter.event_handle(self.coords)

        file_path = os.path.join(self.working_dir, EVENT_FILE)

        with open(file_path) as file:
            data = json.load(file)

            assert data == self.coords

    def tearDown(self):
        try:
            os.remove(os.path.join(self.working_dir, CONFIG_FILE))
        except Exception as e0:
            pass
        try:
            os.remove(os.path.join(self.working_dir, EVENT_FILE))
        except Exception as e1:
            pass


if __name__ == '__main__':
    unittest.main()
