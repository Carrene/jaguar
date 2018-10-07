
from restfulpy.principal import JwtPrincipal, JwtRefreshToken
from nanohttp import context
from bddrest.authoring import response, when, Update, Remove, status

from jaguar.models.membership import User
from jaguar.models.target import Room
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestAddToRoom(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.user = User(
            email='user@example.com',
            title='user',
            access_token='access token',
            reference_id=1
        )
        session.add(cls.user)
        cls.user1 = User(
            email='user1@example.com',
            title='user1',
            access_token='access token1',
            reference_id=2
        )
        session.add(cls.user1)
        cls.blocked1 = User(
            email='blocked1@example.com',
            title='blocked1',
            access_token='access token3',
            reference_id=4
        )
        cls.blocked2 = User(
            email='blocked2@example.com',
            title='blocked2',
            access_token='access token',
            reference_id=6
        )
        cls.room_member = User(
            email='member@example.com',
            title='member',
            access_token='access token',
            reference_id=3
        )
        cls.never = User(
            email='never@example.com',
            title='never',
            access_token='access token',
            add_to_room=False,
            reference_id=7
        )
        session.add(cls.never)
        cls.blocker = User(
            email='blocker@example.com',
            title='blocker',
            access_token='access token4',
            reference_id=5,
            blocked_users=[cls.blocked1, cls.blocked2]
        )
        session.add(cls.blocker)
        room = Room(title='example', type='room', members=[cls.room_member])
        session.add(room)
        session.commit()

    def test_add_user_to_room(self):
        self.login('user@example.com')

        with cas_mockup_server(), self.given(
            'Add to a room',
            '/apiv1/rooms/id:1',
            'ADD',
            form=dict(userId=self.user1.reference_id),
        ):
            assert status == 200
            assert len(response.json['memberIds']) == 2

            when(
                'Already added to the room',
                form=Update(userId=self.room_member.reference_id)
            )
            assert status == '604 Already Added To Target'

            when('User not exists', form=Update(userId=10))
            assert status == '611 User Not Found'

            when(
                'Not allowed to add this person to any room',
                 form=Update(userId=self.never.reference_id)
            )
            assert status == '602 Not Allowed To Add This Person To Any Room'

            when('Room not exist', url_parameters=Update(id='2'))
            assert status == 612

        self.logout()
        self.login('blocked1@example.com')

        with cas_mockup_server(), self.given(
            'Blocked by the target user',
            '/apiv1/rooms/1',
            'ADD',
            form=dict(userId = self.blocker.reference_id)
        ):
            assert status == '601 Not Allowed To Add User To Any Room'

        self.logout()
        self.login('blocker@example.com')

        with cas_mockup_server(), self.given(
            'The blocker can not add the user he blocked',
            '/apiv1/rooms/1',
            'ADD',
            form=dict(userId=4),
        ):
            assert status == '601 Not Allowed To Add User To Any Room'

