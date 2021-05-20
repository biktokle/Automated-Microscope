import importlib
import unittest
from unittest import TestCase
from unittest import mock
from unittest.mock import patch, MagicMock
from undecorated import undecorated

from am_adapters.am_adapter_avi import AMAdapterAVI
from controller.controller import Controller
from notification.publisher import Events


class TestController(TestCase):

    def setUp(self):
        self.controller = Controller()
        self.controller.create_adapters = MagicMock(return_value=(MagicMock(), MagicMock()))

    def test_stop_when_running(self):
        self.controller.executing = True
        self.controller.ed_adapter = MagicMock()
        self.controller.ed_adapter.stop = MagicMock()
        self.controller.stop()
        assert self.controller.ed_adapter.stop.called

    def test_stop_when_not_running(self):
        self.controller.ed_adapter = MagicMock()
        self.controller.ed_adapter.stop = MagicMock()
        self.controller.stop()
        assert not self.controller.ed_adapter.stop.called

    def test_check_if_running(self):
        self.controller.executing = True
        method = MagicMock()
        self.controller.publisher.subscribe(Events.executing_event)(method)
        self.controller.get_detectors()
        assert method.called




if __name__ == '__main__':
    unittest.main()
