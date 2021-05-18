class Event:
    """
    This class represent an event that the event detector has detected.
    """

    def __init__(self, coordinates, microscope_image):
        """
        :param coordinates: the coordinates of the event.
        :param microscope_image: the image that contains the event with the specified coordinates.
        """
        self.coordinates = coordinates
        self.microscope_image = microscope_image

