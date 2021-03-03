import unittest
from controller.controller import Controller
from notification.publisher import Events


class TestController(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_get_detectors(self):
        controller = Controller()
        detectors = controller.get_detectors()
        self.assertEquals(len(detectors), 1, 'There should be a single problem domain at the start')

    def test_set_problem_domain(self):
        controller = Controller()
        problem = controller.set_problem_domain(0)
        self.assertIsNotNone(problem, 'The problem domain is None')
        self.assertIsNone(controller.set_problem_domain(1), 'There should be a single problem domain at the start')

    def test_set_microscope(self):
        controller = Controller()

        def raise_func():
            controller.set_microscope(0)

        self.assertRaises(Exception, raise_func, 'There should be an exception, No problem domain chosen')
        controller.set_problem_domain(0)
        microscope = controller.set_microscope(0)
        self.assertIsNotNone(microscope, 'There should be a microscope for this problem domain')

    def test_set_detector(self):
        controller = Controller()

        def raise_func():
            controller.set_detector(len(controller.detectors) + 1)

        self.assertRaises(Exception, raise_func, 'There should be an exception, index out of range')
        controller.set_detector(0)
        self.assertIsNotNone(controller.chosen_detector, 'The chosen detector shouldnt be none')

    def test_set_image_path(self):
        controller = Controller()

        def raise_func():
            controller.set_image_path('Some Weird Invalid Path')

        self.assertRaises(Exception, raise_func, 'The path is invalid, no exception thrown')
        controller.set_image_path('C:\\Users\\image.jpg')
        self.assertIsNotNone(controller.image_path, 'The image path was set properly but is still None')

    def test_run(self):
        controller = Controller()

        def raise_func():
            controller.run()
            controller.stop()

        self.assertRaises(Exception, raise_func, 'There are should be an exception, not everything is selected')
        controller.set_problem_domain(0)
        self.assertRaises(Exception, raise_func, 'There are should be an exception, not everything is selected')
        controller.set_image_path('C:\\Users\\image.jpg')
        self.assertRaises(Exception, raise_func, 'There are should be an exception, not everything is selected')
        controller.set_detector(0)
        self.assertRaises(Exception, raise_func, 'There are should be an exception, not everything is selected')
        controller.set_microscope(0)

        controller.run()
        controller.stop()

    def test_run_and_try_doing_stuff(self):
        controller = Controller()
        counter = 0

        def increment():
            nonlocal counter
            counter += 1

        controller.set_problem_domain(0)
        controller.set_image_path('C:\\Users\\image.jpg')
        controller.set_detector(0)
        controller.set_microscope(0)

        controller.publisher.subscribe(Events.executing_event)(increment)
        controller.run()

        controller.set_detector(0)
        controller.set_microscope(0)
        controller.run()

        self.assertEquals(counter, 3, 'There should be 3 error events')


if __name__ == '__main__':
    unittest.main()
