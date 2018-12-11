from jaguar.messaging.message_router import MessageRouter
from jaguar.models import Member, Room
from jaguar.tests.helpers import AutoDocumentationBDDTest
from jaguar.messaging.websocket import session_manager


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
        pass

    def test_get_member_by_taget(self):
        members = self.message_router.get_members_by_target(self.room.id)
        assert len(members) == 2
        assert members[0].title == self.member1.title
        assert members[1].title == self.member2.title

    def test_route(self):
        pass

