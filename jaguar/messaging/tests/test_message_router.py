from nanohttp import settings
import aio_pika

from jaguar.messaging.message_router import MessageRouter
from jaguar.messaging.websocket import queue_manager, session_manager
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
        cls.envelop = {'target_id': cls.room.id}

    async def setup(self):
        await session_manager.redis()
        await session_manager.register_session(
            f'member:{self.member1.id}',
            1,
            'test_queue'
        )
        self.queue_name = 'test_queue'
        self.envelop = {'target_id': self.room.id, 'message': 'sample message'}
        self.connection_async = await queue_manager.rabbitmq_async
        self.queue_async = await queue_manager.create_queue_async(self.queue_name)

    def test_get_member_by_taget(self):
        members = self.message_router.get_members_by_target(self.room.id)
        assert len(members) == 2
        assert members[0].title == self.member1.title
        assert members[1].title == self.member2.title

    async def test_route(self):
        number_of_messages = 0
        last_message = None

        await self.setup()
        await queue_manager._channel_async.default_exchange.publish(
            aio_pika.Message(b'Sample message'),
            routing_key='test_queue',
        )

        await self.message_router.route(self.envelop)

        async with self.connection_async:
            async for message in self.queue_async:
                with message.process():
                    number_of_messages += 1

                if number_of_messages == 1:
                    break

        assert number_of_messages == 1

