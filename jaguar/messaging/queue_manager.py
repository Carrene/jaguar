from typing import Callable

import aio_pika
from aio_pika.channel import Channel as RabbitChannel
from nanohttp import settings


class QueueManager:
    _channel__ = None
    queues = None

    def __init__(self):
        self.queues = {}

    @property
    async def rabbitmq(self) -> RabbitChannel:
        if self._channel__ is None:
            connection = await aio_pika.connect(settings.rabbitmq.url)
            self._channel__ = connection.channel()

        return self._channel__

    async def create_queue(self, name: str):
        queue = await self._channel__.declare_queue(name)
        self.queues[name] = queue
        return queue

    async def enqueue(self, queue_name: str, envelop: str):
        await self._channel__.default_exchange.publish(
            aio_pika.Message(
                body=envelop
            ),
            routing_key=queue_name
        )

    async def dequeue(self, queue_name: str, callback: Callable):
        self.queues[queue_name].consume(callback)

