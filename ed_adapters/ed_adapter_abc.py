from abc import ABC, abstractmethod

from notification.publisher import Publisher


class EDAdapter(ABC):
    """
    This class is an abstract Event Detector EDAdapater. It holds the responsibility for communicating with the event
    detector.
    """
    def __init__(self, detector, image_path):
        """
        :param detector: the event detector.
        :param image_path: the path to the directory of the microscope images.
        """
        self.detector = detector
        self.image_path = image_path
        self.running = True
        self.publisher = Publisher()

    @abstractmethod
    def consume_image(self):
        """
        This method consumes an image from the directory with the path self.image_path.
        """
        pass

    @abstractmethod
    def process_image(self, im):
        """
        :param im: an image.
        :return: the image im after processing it.
        """
        pass

    @abstractmethod
    def feed_to_event_detector(self, processed_im, full_path):
        """
        :param processed_im: the processed image.
        :param full_path: the path to the event detector file.
        This method inserted the image as an input to the event detector and act upon its output.
        """
        pass

    def adapter_loop(self):
        """
        This method starts the activation of the adapter.
        """
        print('starting ed')
        while self.running:
            im, full_path = self.consume_image()
            if im is not None:
                processed_im = self.process_image(im)
                self.feed_to_event_detector(processed_im, full_path)

    def stop(self):
        """
        This method stops the activation of the adapter.
        """
        self.running = False

