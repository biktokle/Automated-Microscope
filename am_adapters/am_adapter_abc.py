from abc import ABC, abstractmethod


class AMAdapter(ABC):
    """
    This class is an abstract Event Detector AMAdapater. It holds the responsibility for communicating with the
    microscope
    """

    @abstractmethod
    def activate_microscope(self):
        """
        This method start the microscope activation.
        """
        pass

    def parse_regions(self):
        """
        This method fetches the regions of the area we want to explore in the image.
        """
        pass

    @abstractmethod
    def event_handle(self, coords):
        """
        :param coords: the coordinates in which an event has occurred.
        This method sends a message to microscope to handle an event at the specified coordinates.
        """
        pass
