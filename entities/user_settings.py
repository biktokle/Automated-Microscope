class UserSettings:
    """
    This class holds the settings keys and values that are sent to the microscope.
    """

    def __init__(self, settings_map):
        """
        :param settings_map: the settings keys and values that are sent to the microscope.
        """
        self.settings_map = settings_map
