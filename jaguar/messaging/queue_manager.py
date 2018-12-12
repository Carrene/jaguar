import json
from typing import Callable

import aio_pika
from aio_pika.connection import Connection as RabbitConnection
from nanohttp import settings


class QueueManager:
    _channel = None
    _connection = None
    queues = None

    def __init__(self):
        self.queues = {}

    @property
    async def rabbitmq(self) -> RabbitConnection:
        if self._connection is None:
            self._connection = await aio_pika.connect(settings.rabbitmq.url)

        return self._connection

    async def create_queue(self, name: str):
        if self._channel is None:
            self._channel = await self._connection.channel()

        queue = await self._channel.declare_queue(name)
        self.queues[name] = queue
        return queue

    async def enqueue(self, queue_name: str, envelop: str):
        encoded_envelop = bytes(json.dumps(envelop), 'utf-8')

        async with self._connection.channel() as channel:
            await channel.default_exchange.publish(
                aio_pika.Message(body=encoded_envelop),
                routing_key=queue_name
            )

    async def dequeue(self, queue_name: str, callback: Callable):
        await self.queues[queue_name].consume(callback)

