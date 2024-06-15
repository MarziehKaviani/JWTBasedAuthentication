from pathlib import Path

import pika
from decouple import config
from django.utils.translation import gettext_lazy as _

from authentication.settings import *
from common.settings import *


class RabbitMQConnection:  # TODO get link frrom .env
    def connect(self):
        print('Start Connecting to RabbitMQ...')
        # connection = pika.BlockingConnection(
        connection = pika.BlockingConnection(
            pika.URLParameters('amqp://guest:guest@localhost:5672/'))
        # pika.URLParameters('amqp://admin:admin@rabbitmq:5672/'))

        return connection


RABBIT_MQ_CONNECTION = RabbitMQConnection().connect()
