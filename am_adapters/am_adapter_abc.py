from abc import ABC, abstractmethod


class AMAdapter(ABC):
    """
    This class is an abstract Event Detector AMAdapater. It holds the responsibility for communicating with the
    microscope
    """
    def __init__(self, user_settings):
        self.user_settings = user_settings

    @abstractmethod
    def consume_coords(self):
        """
        This method fetches the coordinates of the area we want to explore in the image.
        """
        pass

    @abstractmethod
    def activate_microscope(self, coords):
        """
        :param coords: the coordinates in which an event has occurred.
        This method sends a message to microscope to handle an event at the specified coordinates.
        """
        pass
