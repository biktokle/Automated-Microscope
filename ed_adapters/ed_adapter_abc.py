from abc import ABC, abstractmethod
from subprocess import Popen

from communication import protocol, client
from notification.publisher import Publisher


class EDAdapter(ABC):
    """
    This class is an abstract Event Detector EDAdapater. It holds the responsibility for communicating with the event
    detector.
    """
    def __init__(self, detector, working_dir):
        """
        :param detector: the event detector.
        :param working_dir: the path to the working directory.
        """
        self.detector = detector
        self.working_dir = working_dir
        self.running = True
        self.publisher = Publisher()
        self.client = None
        self.server = None

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

    def setup_communication(self):
        """
        This method sets up a communication channel with the event detector program.
        """
        free_port = client.get_free_port()
        process = Popen(f'python "{self.detector.detector_path}" {client.get_free_port()}')
        self.client = client.Client(free_port)
        return process

    def stop_communication(self):
        self.client.stop_communication()
        self.server.wait()

    @abstractmethod
    def initialize_adapter(self):
        pass

    def adapter_loop(self):
        """
        This method starts the activation of the adapter.
        """
        print('starting ed')
        self.initialize_adapter()
        self.server = self.setup_communication()
        while self.running:
            im, full_path = self.consume_image()
            if im is not None:
                processed_im = self.process_image(im)
                self.feed_to_event_detector(processed_im, full_path)

    def stop(self):
        """
        This method stops the activation of the adapter.
        """
        self.stop_communication()
        self.running = False

