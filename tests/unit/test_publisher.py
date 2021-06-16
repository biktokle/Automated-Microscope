from unittest import TestCase
from unittest.mock import MagicMock

from notification.publisher import Publisher

def test_func(x):
    x.append('test')

class TestPublisher(TestCase):

    def setUp(self):
        self.publisher = Publisher()

    def test_called(self):
        method = MagicMock()
        self.publisher.subscribe('test')(method)
        self.publisher.publish('test')
        assert method.called

    def test_called_with_param(self):
        self.publisher.subscribe('test')(test_func)
        x = []
        self.publisher.publish('test', x)
        assert x[0] == 'test'

    def test_called_without_param(self):
        thrown = False
        self.publisher.subscribe('test')(test_func)
        try:
            self.publisher.publish('test')
        except TypeError:
            thrown = True
        assert thrown

    def test_different_pub_sub(self):
        method = MagicMock()
        self.publisher.subscribe('test')(method)
        self.publisher.publish('test1')
        assert not method.called

    def test_two_subs(self):
        method = MagicMock()
        self.publisher.subscribe('test')(method)
        self.publisher.publish('test')
        self.publisher.publish('test')
        assert method.call_count == 2

    def test_two_pubs(self):
        method = MagicMock()
        method1 = MagicMock()
        self.publisher.subscribe('test')(method)
        self.publisher.subscribe('test')(method1)
        self.publisher.publish('test')
        assert method.called and method1.called

    

