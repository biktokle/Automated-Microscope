from pyfakefs.fake_filesystem_unittest import TestCase
from ed_adapters.ed_adapter_default import EDAdapterDefault, IMAGES_PATH
from unittest.mock import Mock
from exceptions.exceptions import *
import os


class TestEDAdapterDefault(TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        self.detector_mock = Mock()
        self.working_dir = '/some/working/dir'
        self.ed_adapter = EDAdapterDefault(self.detector_mock, self.working_dir)

    def test_consume_image_no_file(self):
        self.fs.create_dir(self.working_dir)
        self.assertRaises(FileNotFoundException, self.ed_adapter.consume_image)

    def test_consume_image_directory_not_set_up(self):
        self.ed_adapter.working_dir = None
        self.assertRaises(DirectoryNotSetUpException, self.ed_adapter.consume_image)

    def test_consume_image_ambiguous_files(self):
        self.fs.create_file(os.path.join(self.working_dir, IMAGES_PATH, 'image1.tif'))
        self.fs.create_file(os.path.join(self.working_dir, IMAGES_PATH, 'image2.tif'))
        self.assertRaises(AmbiguousFilesException, self.ed_adapter.consume_image)




