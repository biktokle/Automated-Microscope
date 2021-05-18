import pathlib
import os
from entities.microscope_image import MicroscopeImage


class EventDetector:
    """
    This class holds the data and path of the event detector.
    """
    def __init__(self, path):
        """
        :param path: the inserted path of the event detector.
        """
        self.path = path
        self.detector_path, self.image, self.description = self.get_data()
        self.name = os.path.basename(path)

    def get_data(self):
        """
        :return: the file path, a sample image and a description of the event detector.
        """
        detector_path = None
        image = None
        description = ""
        for name in os.listdir(self.path):
            suffix = pathlib.Path(os.path.join(self.path, name)).suffix
            prefix = pathlib.Path(os.path.join(self.path, name)).stem
            if prefix != self.name:
                continue
            full_path = os.path.join(self.path, name)
            if suffix == '.txt':
                self.description = open(full_path, "r").read()
            elif suffix == '.py':
                self.detector_path = full_path
            else:
                try:
                    self.image = MicroscopeImage(full_path)
                except Exception as e:
                    pass

        return detector_path, image, description

    def show_image(self):
        """
        This method shows the sample image of the event detector.
        """
        try:
            self.image.show()
        except Exception as e:
            pass
