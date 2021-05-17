import pathlib
import os
from entities.microscope_image import MicroscopeImage


class EventDetector:
    def __init__(self, path):
        self.path = path
        self.detector_path = None
        self.image = None
        self.description = ""
        self.name = os.path.basename(path)
        self.get_data()

    def get_data(self):
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

    def show_image(self):
        try:
            self.image.show()
        except Exception as e:
            pass
