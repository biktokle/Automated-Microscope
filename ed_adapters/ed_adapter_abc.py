from abc import ABC, abstractmethod


class EDAdapter(ABC):

    # @abstractmethod
    # def __init__(self, path):
    #     self.path = path

    @abstractmethod
    def consume_image(self):
        pass

    @abstractmethod
    def process_image(self, im):
        pass

    @abstractmethod
    def feed_to_event_detector(self, processed_im):
        pass

    def adapter_loop(self):
        while 1:
            print('starting ed')
            im = self.consume_image()
            processed_im = self.process_image(im)
            self.feed_to_event_detector(processed_im)

