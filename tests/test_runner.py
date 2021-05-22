from tests.e2e import test_cell_detection_e2e
from tests.integration import test_controller_integration
import unittest

from tests.unit import test_ed_adapter_default, test_am_adapter_avi, test_controller


def suite_tests():
    # initialize the test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # add tests to the test suite
    suite.addTests(loader.loadTestsFromModule(test_cell_detection_e2e))
    suite.addTests(loader.loadTestsFromModule(test_controller_integration))
    suite.addTests(loader.loadTestsFromModule(test_ed_adapter_default))
    suite.addTests(loader.loadTestsFromModule(test_am_adapter_avi))
    suite.addTests(loader.loadTestsFromModule(test_am_adapter_avi))
    suite.addTests(loader.loadTestsFromModule(test_controller))
    return suite


if __name__ == '__main__':
    # initialize a runner, pass it your suite and run it
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite_tests())
