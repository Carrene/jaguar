import aio_pika
from nanohttp import settings

from jaguar.messaging.queue_manager import QueueManager
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

#        self.connection_async = await self.queue_manager.rabbitmq_async
#        self.queue_async = await self.queue_manager.create_queue_async(
#            self.queue_name
#        )

#    async def test_dequeue_async(self):
#        await self.setup()
#
#        await self.queue_manager._channel_async.default_exchange.publish(
#            aio_pika.Message(b'Sample message'),
#            routing_key='test_queue',
#        )
#
#        await self.queue.consume(self.callback)
#        await self.connection.close()
#
#        assert self.number_of_callbacks == 1
#        assert self.last_message == b'Sample message'

    async def test_enqueue(self):
        await self.setup()
        connection = self.queue_manager.rabbitmq
        queue = self.queue_manager.create_queue(self.queue_name)
        self.queue_manager.enqueue('test_queue', self.envelop)
        connection.close()

        connection_async = await self.queue_manager.rabbitmq_async
        queue_async = await self.queue_manager.create_queue_async(
            self.queue_name
        )
        async for message in queue_async:
            with message.process():
                assert message.body.encode() == json.dumps(self.envelop)
                break

