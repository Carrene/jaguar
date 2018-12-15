import json
import threading

import aio_pika

from jaguar.messaging.queue_manager import QueueManager
from jaguar.messaging.websocket import queue_manager
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestQueueManager(AutoDocumentationBDDTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.number_of_callbacks = 0
        cls.last_message = None

    @classmethod
    async def callback(cls, message: aio_pika.IncomingMessage):
        with message.process():
            cls.number_of_callbacks += 1
            cls.last_message = message.body

    async def setup(self):
        self.queue_name = 'test_queue'
        self.envelop = {'target_id': 1, 'message': 'sample message'}
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
                assert message.body == bytes(json.dumps(self.envelop), 'utf-8')
                break

    async def test_dequeue_async(self):
        await self.setup()
        await self.queue_manager.dequeue_async(self.queue_name, self.callback)

    def _enqueue_threadsafe(self):
        queue_manager.enqueue(self.queue_name, self.envelop)

    async def test_enqueue(self):
        await self.setup()
        connection = queue_manager.rabbitmq
        queue = queue_manager.create_queue(self.queue_name)
        async for message in self.queue:
            with message.process():
                assert message.body.encode() == json.dumps(self.envelop)
                break

