import pika
from event_handlers import LogHandler
# Assuming you have a serializer class
from serializers import LogEventDeSerializer


def log_callback(ch, method, properties, body):
    deserialized_message = LogEventDeSerializer(
        'protobuf').deserialize(body)  # TODO serializer type
    LogHandler(deserialized_message).handle_event(deserialized_message)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume_info_logs():  # TODO logs not just info
    print('Logs event consumer started listening...')
    rabbitmq_url = 'amqp://guest:guest@localhost:5672/'
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='direct')
    channel.queue_declare(queue='logs_queue', durable=True)
    channel.queue_bind(exchange='logs', queue='logs_queue', routing_key='info')
    channel.basic_consume(queue='logs_queue', on_message_callback=log_callback)
    channel.start_consuming()


if __name__ == "__main__":
    consume_info_logs()
