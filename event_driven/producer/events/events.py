from .base import Event


class LogEvent(Event):
    level: str
    message: str
