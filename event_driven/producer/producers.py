import os

import pika
# from celery import shared_task
from django.conf import settings


class Producer:
    def __init__(self, rabbitmq_url=os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')):
        self.rabbitmq_url = rabbitmq_url

    def produce_message(rabbitmq_url, serialized_message, exchange_name, exchange_type, routing_key, delivery_mode=2):
        channel = settings.RABBIT_MQ_CONNECTION.channel()
        channel.exchange_declare(
            exchange=exchange_name, exchange_type=exchange_type)
        channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=serialized_message,
            properties=pika.BasicProperties(
                delivery_mode=delivery_mode,
            )
        )
