from abc import ABC, abstractmethod

from notification.publisher import Publisher


class EDAdapter(ABC):
    def __init__(self, detector, image_path):
        self.detector = detector
        self.image_path = image_path
        self.running = True
        self.publisher = Publisher()

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
        print('starting ed')
        while self.running:
            im = self.consume_image()
            if im is not None:
                processed_im = self.process_image(im)
                self.feed_to_event_detector(processed_im)

    def stop(self):
        self.running = False

