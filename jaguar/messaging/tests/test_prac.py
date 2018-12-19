import aio_pika
from nanohttp import settings

from jaguar.messaging.queue_manager import QueueManager
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestQueueManager(AutoDocumentationBDDTest):
    number_of_callbacks = 0
    last_message = None

#    @classmethod
#    def setup_class(cls):
#        super().setup_class()
#        cls.number_of_callbacks = 0
#        cls.last_message = None

    @classmethod
    async def callback(self, message: aio_pika.IncomingMessage):
        with message.process():
            self.number_of_callbacks += 1
            self.last_message = message.body

    async def setup(self):
        self.queue_name = 'test_queue'
        self.envelop = {'target_id': 1, 'message': 'sample message'}
        self.queue_manager = QueueManager()

        self.connection = await self.queue_manager.rabbitmq_async
        self.queue = await self.queue_manager.create_queue_async(self.queue_name)

    async def test_dequeue_async(self):
        await self.setup()

#        envelop = {'target_id': 1, 'message': 'sample message'}
#        queue_manager = QueueManager()
#        connection = await queue_manager.rabbitmq_async
#        channel = await connection.channel()
#        queue = await channel.declare_queue('test_queue')

        import pudb; pudb.set_trace()  # XXX BREAKPOINT
        await self.queue_manager._channel.default_exchange.publish(
            aio_pika.Message(b'Hello World!'),
            routing_key='test_queue',
        )
        self.queue = await self.channel.declare_queue('test_queue')

        queue = await queue_manager.create_queue_async('test_queue')
        print('hi')

        await self.queue.consume(self.callback)

        await self.connection.close()

        assert self.number_of_callbacks == 1
        assert self.last_message != None


