import flatbuffers

from event_driven.serializers_format.formats.flatbuffer.Events import logevent
from event_driven.serializers_format.formats.protobuf.event_pb2 import \
    logevent as pb_logevent

from .events.events import LogEvent


class LogEventSerializer:
    def __init__(self, serializer_format) -> None:
        if serializer_format not in ['protobuf', 'flatbuffer']:
            raise Exception(
                f'Unsuported serializer format: {serializer_format}')

        self.serializer_format = serializer_format

    def serialize(self, event: LogEvent):
        if self.serializer_format == 'protobuf':
            return self.protobuf_serialize(event)
        elif self.serializer_format == 'flatbuffer':
            return self.flatbuffer_serializer(event)

    def deserialize(self, serialized_event):
        if self.serializer_format == 'protobuf':
            return self.protobuf_deserialize(serialized_event)
        elif self.serializer_format == 'flatbuffer':
            return self.flatbuffer_deserializer(serialized_event)

    def flatbuffer_serializer(self, event: LogEvent):
        builder = flatbuffers.Builder(1024)
        name_value = builder.CreateString(event['name'])
        timestamp_value = builder.CreateString(
            event['fields'].get('timestamp', '')['value'])
        source_value = builder.CreateString(
            event['fields'].get('source', '')['value'])
        serializer_format_value = builder.CreateString(
            event['fields'].get('serializer_format', '')['value'])
        message = builder.CreateString(
            event['fields'].get('message', '')['value'])
        level = builder.CreateString(event['fields'].get('level', '')['value'])

        logevent.Start(builder)
        logevent.logeventAddName(builder, name_value)
        logevent.logeventAddTimestamp(builder, timestamp_value)
        logevent.logeventAddSource(builder, source_value)
        logevent.logeventAddSerializerFormat(builder, serializer_format_value)
        logevent.logeventAddMessage(builder, message)
        logevent.logeventAddLevel(builder, level)
        logevent_instance = logevent.logeventEnd(builder)
        builder.Finish(logevent_instance)
        return builder.Output()

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
        return deserialized_event

    def protobuf_serialize(self, event: LogEvent):
        pb_event = pb_logevent()
        pb_event.name = event.name
        pb_event.timestamp = event.timestamp.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        pb_event.source = event.source
        pb_event.serializer_format = event.serializer_format
        pb_event.message = event.message
        pb_event.level = event.level
        return pb_event.SerializeToString()

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


if __name__ == '__main__':

    event = {'name': 'LogE', 'fields': {
        'level': {'type': 'str', 'value': '4'},
        'message': {'type': 'int', 'value': 'dsfcc'},
        'name': {'type': 'str', 'value': 'dsfcc'},
        'timestamp': {'type': 'datetime.datetime', 'value': 'dsfcc'},
        'source': {'type': 'str', 'value': 'dsfcc'},
        'serializer_format': {'type': 'str', 'value': 'dsfcc'},
    }}
    serialized_message = LogEventSerializer('flatbuffer').serialize(event)
    print('\nflatbuffer serialized data: ', serialized_message, '\n')
    print('flatbuffer deserialized data: ', LogEventSerializer(
        'flatbuffer').deserialize(serialized_message), '\n')

    # protobuf
    serializer = LogEventSerializer('protobuf')
    serialized_data = serializer.serialize(event)
    print('protobuf serialized data: ', serialized_data, '\n')

    deserialized_event = serializer.deserialize(serialized_data)
    print('protobuf deserialized data: ', deserialized_event, '\n')
