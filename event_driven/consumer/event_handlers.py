from handlers.base import Handler
from serializers import LogEventDeSerializer


class LogHandler(Handler):
    event_name = 'logs'

    def handle_event(self, data):
        super().handle_event(data)
        print('recieveeed data in handlerrr dadaaa: ', data)


def log_callback(ch, method, properties, body):
    deserialized_message = LogEventDeSerializer(
        'protobuf').deserialize(body)  # TODO serializer type
    LogHandler(deserialized_message).handle_event(deserialized_message)
    ch.basic_ack(delivery_tag=method.delivery_tag)
