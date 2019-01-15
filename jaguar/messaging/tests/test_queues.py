import json

from jaguar.messaging import queues
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestQueueManager(AutoDocumentationBDDTest):

    async def test_push_pop_async(self):
        queue_name = 'test_queue'
        envelop = {'target_id': 1, 'message': 'sample message'}
        await queues.push_async(queue_name, envelop)

        message = await queues.pop_async(queue_name)
        assert message == envelop


