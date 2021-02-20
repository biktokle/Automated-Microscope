import imageio
import matplotlib.pyplot as plt

class MicroscopeImage:

    def __init__(self, path):
        self.image = imageio.imread(path)

    def show(self):
        plt.imshow(self.image)
        plt.show()
