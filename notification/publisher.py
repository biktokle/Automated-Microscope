from enum import Enum


class Publisher(object):
    def __init__(self):
        self.observers = {}

    def subscribe(self, event_name):
        def _subscribe(fn):
            if event_name not in self.observers.keys():
                self.observers[event_name] = []

            self.observers[event_name].append(fn)
            return fn

        return _subscribe

    def publish(self, event_name, *args, **kwargs):
        if event_name not in self.observers:
            return
        for fn in self.observers[event_name]:
            fn(*args, **kwargs)


class Events(Enum):
    popup_event = 'popup'
    image_event = 'image'
    model_detection_event = 'model_detection'
