from abc import ABC, abstractmethod


class AMAdapter(ABC):
    def __init__(self):
        self.running = True

    @abstractmethod
    def consume_coords(self):
        pass

    @abstractmethod
    def read_actions_config(self):
        pass

    @abstractmethod
    def translate_actions(self, actions, coords):
        pass

    @abstractmethod
    def activate_microscope(self, actions):
        pass

    def adapter_loop(self):
        print('starting am')
        while self.running:
            cords = self.consume_coords()
            if cords is not None:
                acts = self.read_actions_config()
                acts = self.translate_actions(acts, cords)
                self.activate_microscope(acts)

    def stop(self):
        self.running = False

