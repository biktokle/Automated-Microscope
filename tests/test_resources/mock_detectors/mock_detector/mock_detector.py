import sys
from skimage import io
from communication import protocol, server

DETECT = 'DETECT'
port = int(sys.argv[1])
class Detector(server.Server):

    def __init__(self, port, chosen_protocol, threshold=0.5):
        self.threshold = threshold
        self.counter = 0
        super().__init__(port, chosen_protocol)

    def handle_request(self, data):
        did_dict = {
            'xmin': int(200),
            'ymin': int(200),
            'xmax': int(220),
            'ymax': int(220)
        }
        if self.counter < 3:
            self.counter += 1
            return None, None

        return did_dict, None







if __name__=='__main__':
    Detector(port, protocol.DETECT)
