import unittest
from unittest import TestCase
import os

class TestController(TestCase):

    def setUp(self):
        self.hey = 'Hello'


    def tearDown(self):
        print(self.hey)


if __name__ == '__main__':
    unittest.main()


def execute(test_controller):
    pass
