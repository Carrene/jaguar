import json
from typing import Callable

import aio_pika
import pika
from aio_pika.connection import Connection as RabbitConnection
from nanohttp import settings


class QueueManager:
    _channel_async = None
    _connection_async = None
    _channel = None
    _connection = None
    queues = None

    def __init__(self):
        self.queues = {}

    @property
    async def rabbitmq_async(self) -> RabbitConnection:
        if self._connection_async is None:
            self._connection_async = await aio_pika.connect(settings.rabbitmq.url)

        return self._connection_async

    @property
    def rabbitmq(self):
        if self._connection is None:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters('127.0.0.1')
            )

        return self._connection

    async def create_queue_async(self, name: str):
        connection_async = await self.rabbitmq_async
        if self._channel_async is None:
            self._channel_async = await connection_async.channel()

        queue = await self._channel_async.declare_queue(name)
        self.queues[name] = queue
        return queue

    def create_queue(self, name: str):
        connection = self.rabbitmq
        if self._channel is None:
            self._channel = connection.channel()

        queue = self._channel.queue_declare(name)
        self.queues[name] = queue
        return queue

    async def enqueue_async(self, queue_name: str, envelop: str):
        encoded_envelop = json.dumps(envelop).encode()

        await self._channel_async.default_exchange.publish(
            aio_pika.Message(body=encoded_envelop),
            routing_key=queue_name
        )

    async def dequeue_async(self, queue_name: str, callback: Callable):
        await self.queues[queue_name].consume(callback)

    def enqueue(self, queue_name: str, envelop: str):
        encoded_envelop = json.dumps(envelop).encode()

        self._channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=encoded_envelop
        )


queue_manager = QueueManager()

