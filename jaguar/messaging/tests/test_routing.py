import pytest

from jaguar.messaging import queues, sessions, router
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

    def test_get_member_by_taget(self):
        members = router.get_members_by_target(self.room.id)
        assert len(members) == 2
        assert members[0].title == self.member1.title
        assert members[1].title == self.member2.title

    @pytest.mark.asyncio
    async def test_route(self):
        await sessions.dispose()
        await sessions.flush_all()
        await queues.dispose_async()
        await queues.flush_all_async()

        queue_name = 'test_queue'
        session_id = '1'

        await sessions.flush_all()
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


