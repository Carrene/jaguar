import json
import threading

import aio_pika

from jaguar.messaging.queues import QueueManager
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestQueueManager(AutoDocumentationBDDTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.number_of_callbacks = 0
        cls.last_message = None

    @classmethod
    async def callback(self, message: aio_pika.IncomingMessage):
        with message.process():
            self.number_of_callbacks += 1
            self.last_message = message.body

    async def setup(self):
        self.queue_name = 'test_queue'
        self.envelop = {'targetId': 1, 'message': 'sample message'}
        self.queue_manager = QueueManager()

        self.connection = await self.queue_manager.rabbitmq_async
        self.queue = await self.queue_manager.create_queue_async(self.queue_name)

    async def test_enqueue_async(self):
        await self.setup()
        await self.queue_manager.enqueue_async(
            self.queue_name,
            self.envelop
        )

        async for message in self.queue:
            with message.process():
                assert message.body == json.dumps(self.envelop).encode()
                break
        await self.connection.close()

    async def test_dequeue_async(self):
        await self.setup()

        await self.queue_manager._channel_async.default_exchange.publish(
            aio_pika.Message(b'Sample message'),
            routing_key='test_queue',
        )

        await self.queue.consume(self.callback)
        await self.connection.close()

        assert self.number_of_callbacks == 1
        assert self.last_message == b'Sample message'

