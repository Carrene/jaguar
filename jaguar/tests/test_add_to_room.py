
from restfulpy.orm import DBSession
from restfulpy.principal import JwtPrincipal, JwtRefreshToken
from nanohttp import context
from bddrest.authoring import response, when, Update, Remove, status

from jaguar.models.membership import User
from jaguar.models.target import Room
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestAddToRoom(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user = User(
            email='user@example.com',
            title='user',
            password='123456',
        )
        blocked1 = User(
            email='blocked1@example.com',
            title='blocked1',
            password='123456',
        )
        room_member = User(
            email='member@example.com',
            title='member',
            password='123456',
        )
        never = User(
            email='never@example.com',
            title='never',
            password='123456',
            add_to_room=False,
        )
        blocker = User(
            email='blocker@example.com',
            title='blocker',
            password='123456',
        )
        blocked2 = User(
            email='blocked2@example.com',
            title='blocked2',
            password='123456',
        )
        blocker.blocked_users.append(blocked1)
        blocker.blocked_users.append(blocked2)
        room = Room(title='example', type='room')
        room.members.append(room_member)
        session.add_all(
            [user, blocker, room, never]
        )
        session.commit()

    def test_add_user_to_room(self):
        self.login(
            'user@example.com',
            '123456',
            '/apiv1/tokens',
            'CREATE'
        )

        with self.given(
            'Add to  a room',
            '/apiv1/rooms/id:1',
            'ADD',
            form=dict(userId=1),
        ):
            assert status == 200
            assert len(response.json['memberIds']) == 2

            when('Already added to the room', form=Update(userId=5))
            assert status == '604 Already Added To Target'

            when('User not exists', form=Update(userId=10))
            assert status == '611 User Not Found'

            when('Not allowed to add this person to any room',
                 form=Update(userId=6)
                 )
            assert status == '602 Not Allowed To Add This Person To Any Room'

            when('Room not exist', url_parameters=Update(id='2'))
            assert status == 612


        self.logout()
        self.login(
            'blocked1@example.com',
            '123456',
            '/apiv1/tokens',
            'CREATE'
        )

        with self.given(
            'Blocked by the target user',
            '/apiv1/rooms/1',
            'ADD',
            form=dict(userId = 2)
        ):
            assert status == '601 Not Allowed To Add User To Any Room'

        self.logout()
        self.login(
            'blocker@example.com',
            '123456',
            '/apiv1/tokens',
            'CREATE'
        )

        with self.given(
            'The blocker can not add the user he blocked',
            '/apiv1/rooms/1',
            'ADD',
            form=dict(userId=4),
        ):
            assert status == '601 Not Allowed To Add User To Any Room'

