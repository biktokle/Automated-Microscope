from abc import ABC, abstractmethod
from notification.publisher import Publisher, Events


class AMAdapter(ABC):
    """
    This class is an abstract Event Detector AMAdapater. It holds the responsibility for communicating with the
    microscope
    """
    def __init__(self, user_settings, microscope_manual):
        self.user_settings = user_settings
        self.microscope_manual = microscope_manual
        self.running = True
        self.publisher = Publisher()
        self.publisher.subscribe(Events.image_event)(self.activate_microscope)

    @abstractmethod
    def consume_coords(self):
        """
        This method fetches the coordinates of the area we want to explore in the image.
        """
        pass

    # @abstractmethod
    # def read_actions_config(self):
    #     pass
    #
    # @abstractmethod
    # def translate_actions(self, actions, coords):
    #     pass

    @abstractmethod
    def activate_microscope(self, coords):
        """
        :param coords: the coordinates in which an event has occurred.
        This method sends a message to microscope to handle an event at the specified coordinates.
        """
        pass

    def adapter_loop(self):
        """
        This method starts the activation of the adapter.
        """
        print('starting am')
        while self.running:
            cords = self.consume_coords()
            if cords is not None:
                self.activate_microscope(cords)

    def stop(self):
        """
        This method stops the activation of the adapter.
        """
        self.running = False


