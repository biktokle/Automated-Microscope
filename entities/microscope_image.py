from PIL import ImageTk
from PIL import Image


class MicroscopeImage:
    """
    This class holds a microscope image's data.
    """
    def __init__(self, image):
        """
        :param image: a 2d-array of image pixels.
        """
        self.image = image

    def get_tkinter_image(self):
        """
        :return: a rendered tkinter image to present in the UI from the self.image member.
        """
        load = Image.fromarray(self.image)
        render = ImageTk.PhotoImage(load)
        return render
