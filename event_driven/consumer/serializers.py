import os
import sys

from serializers_format.formats.flatbuffer.Events import logevent
from serializers_format.formats.protobuf.event_pb2 import \
    logevent as pb_logevent

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


class LogEventDeSerializer:
    def __init__(self, serializer_format) -> None:

        if serializer_format not in ['protobuf', 'flatbuffer']:
            raise Exception(
                f'Unsuported serializer format: {serializer_format}')
        self.serializer_format = serializer_format

    def deserialize(self, serialized_event):
        if self.serializer_format == 'protobuf':
            return self.protobuf_deserialize(serialized_event)
        elif self.serializer_format == 'flatbuffer':
            return self.flatbuffer_deserializer(serialized_event)

    def flatbuffer_deserializer(self, serialized_event):
        buf = memoryview(serialized_event)
        logevent_instance = logevent.logevent.GetRootAslogevent(buf, 0)

        name = logevent_instance.Name()
        timestamp = logevent_instance.Timestamp()
        source = logevent_instance.Source()
        serializer_format = logevent_instance.SerializerFormat()
        message = logevent_instance.Message()
        level = logevent_instance.Level()

        deserialized_event = {
            'name': name.decode('utf-8'),
            'fields': {
                'timestamp': {'type': 'datetime.datetime', 'value': timestamp.decode('utf-8')},
                'source': {'type': 'str', 'value': source.decode('utf-8')},
                'serializer_format': {'type': 'str', 'value': serializer_format.decode('utf-8')},
                'message': {'type': 'str', 'value': message.decode('utf-8')},
                'level': {'type': 'str', 'value': level.decode('utf-8')}
            }
        }

    def protobuf_deserialize(self, serialized_event):
        pb_event = pb_logevent()
        pb_event.ParseFromString(serialized_event)

        deserialized_event = {
            'name': pb_event.name,
            'fields': {
                'timestamp': {'type': 'datetime.datetime', 'value': pb_event.timestamp},
                'source': {'type': 'str', 'value': pb_event.source},
                'serializer_format': {'type': 'str', 'value': pb_event.serializer_format},
                'message': {'type': 'str', 'value': pb_event.message},
                'level': {'type': 'str', 'value': pb_event.level}
            }
        }
        return deserialized_event
