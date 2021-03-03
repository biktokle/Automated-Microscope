import imageio
import matplotlib.pyplot as plt
from PIL import ImageTk
from PIL import Image


class MicroscopeImage:
    def __init__(self, image):
        self.image = image

    def get_tkinter_image(self):
        load = Image.fromarray(self.image)
        render = ImageTk.PhotoImage(load)
        return render
