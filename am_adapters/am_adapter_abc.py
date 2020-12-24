from abc import ABC, abstractmethod


class AMAdapter(ABC):


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
        while 1:
            print('starting am')
            cords = self.consume_coords()
            acts = self.read_actions_config()
            acts = self.translate_actions(acts, cords)
            self.activate_microscope(acts)

