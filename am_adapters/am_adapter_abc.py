from abc import ABC, abstractmethod
from notification.publisher import Publisher, Events


class AMAdapter(ABC):
    def __init__(self, user_settings, microscope_manual):
        self.user_settings = user_settings
        self.microscope_manual = microscope_manual
        self.running = True
        self.publisher = Publisher()
        self.publisher.subscribe(Events.image_event)(self.activate_microscope)

    @abstractmethod
    def consume_coords(self):
        pass

    # @abstractmethod
    # def read_actions_config(self):
    #     pass
    #
    # @abstractmethod
    # def translate_actions(self, actions, coords):
    #     pass

    @abstractmethod
    def activate_microscope(self, coords):
        pass

    def adapter_loop(self):
        print('starting am')
        while self.running:
            cords = self.consume_coords()
            if cords is not None:
                acts = self.action_configuration
                acts = self.translate_actions(acts, cords)
                self.activate_microscope(acts)

    def stop(self):
        self.running = False


