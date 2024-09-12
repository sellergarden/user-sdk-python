from enum import Enum


class EventType(Enum):
    API = "api"


class Event:
    def __init__(self, name, type: EventType):
        self.name = name
        self.type = type
