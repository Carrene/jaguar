import aio_pika

from jaguar.messaging.queues import QueueManager
from jaguar.messaging.routing import MessageRouter
from jaguar.messaging.sessions import session_manager
from jaguar.models import Member, Room
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestMessageRouter(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.member1 = Member(
            email='member1@example.com',
            title='member1',
            access_token='access token',
            reference_id=1
        )
        cls.member2 = Member(
            email='member2@example.com',
            title='member2',
            access_token='access token',
            reference_id=2
        )
        cls.room = Room(
            title='room1',
            members=[cls.member1, cls.member2]
        )
        session.add(cls.room)
        session.commit()

        cls.message_router = MessageRouter()

    async def setup(self):
        await session_manager.redis()
        await session_manager.register_session(
            f'member:{self.member1.id}',
            1,
            'test_queue'
        )
        self.queue_name = 'test_queue'
        self.envelop = {
            'targetId': self.room.id,
            'message': 'sample message',
            'senderId': 1,
            'isMine': True
        }
        self.queue_manager = QueueManager()
        self.queue_async = await self.queue_manager \
            .create_queue_async(self.queue_name)

    def test_get_member_by_taget(self):
        members = self.message_router.get_members_by_target(self.room.id)
        assert len(members) == 2
        assert members[0].title == self.member1.title
        assert members[1].title == self.member2.title

    async def test_route(self):
        number_of_messages = 0
        last_message = None

        await self.setup()
        await self.queue_manager._channel_async.default_exchange.publish(
            aio_pika.Message(b'Sample message'),
            routing_key='test_queue',
        )

        await self.message_router.route(self.envelop)

        async with self.queue_manager._connection_async:
            async for message in self.queue_async:
                with message.process():
                    number_of_messages += 1

                if number_of_messages == 1:
                    break

        assert number_of_messages == 1

