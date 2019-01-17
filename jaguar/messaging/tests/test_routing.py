import pytest

from jaguar.messaging import sessions, router, queues
from jaguar.models import Member, Room
from jaguar.messaging.tests.conftest import AsyncTest


class TestMessageRouter(AsyncTest):

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

    @pytest.mark.asyncio
    async def test_route(self, asyncpg):
        queue_name = 'test_queue'
        session_id = '1'

        await sessions.register_session(
            self.member1.id,
            session_id,
            queue_name
        )

        envelop = {
            'targetId': self.room.id,
            'message': 'sample message',
            'senderId': 1,
            'isMine': True
        }
        await router.route(envelop)

        message = await queues.pop_async(queue_name)
        assert message == envelop


