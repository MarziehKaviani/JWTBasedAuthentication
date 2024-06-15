class Handler:

    event_name = None

    def __init__(self, deserialized_message) -> None:
        self.deserialized_message = deserialized_message

    @staticmethod
    def handle_event(self):
        pass
