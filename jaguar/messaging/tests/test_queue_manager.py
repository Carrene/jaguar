from jaguar.messaging.queue_manager import QueueManager
from jaguar.tests.helpers import AutoDocumentationBDDTest
from jaguar.messaging.message_router import MessageRouter


class TestQueueManager(AutoDocumentationBDDTest):

    def setup(self):
        self.queue_manager = QueueManager()

    async def test_rabbitmq(self):
        await self.queue_manager.rabbitmq

        await self.queue_manager.create_queue('test_queue')

