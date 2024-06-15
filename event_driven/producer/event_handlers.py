from .handlers.base import Handler
from .serializers import LogEventSerializer


class LogHandler(Handler):
    event_name = 'logs'

    def handle_event(self, data):
        super().handle_event(data)
        print('recieveeed data in handlerrr dadaaa: ', data)


def log_callback(ch, method, properties, body):
    print('in callbacck')
    deserialized_message = LogEventSerializer(
        'protobuf').deserialize(body)  # TODO serializer type
    LogHandler(deserialized_message).handle_event(deserialized_message)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print('end of log callback')
