
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
            id=1,
            email='already.added@example.com',
            title='example',
            password='123456',
        )
        user.is_active = True
        room_member = User(
            id=2,
            email='member@example.com',
            title='member',
            password='123456',
        )
        never_add_to_room = User(
            id=3,
            email='never.add@example.com',
            title='never',
            password='123456',
            add_to_room=False,
        )
        block_the_user = User(
            id=4,
            email='block@example.com',
            title='block',
            password='123456',
        )
        block_the_user.is_active = True
        lover_lock = User(
            id=5,
            email='lover@example.com',
            title='lover',
            password='123456',
        )
        block_the_user.blocked_users.append(user)
        block_the_user.blocked_users.append(lover_lock)
        room = Room(title='example', type='room')
        room.members.append(room_member)
        session.add_all(
            [user, block_the_user, room, never_add_to_room]
        )
        session.commit()

    def test_add_user_to_room(self):
        self.login(
            'already.added@example.com',
            '123456',
            '/apiv1/tokens',
            'CREATE'
        )
        with self.given(
            'Add to  a room',
            '/apiv1/rooms/1',
            'ADD',
            form=dict(user_id=1),
        ):
            assert status == 200
            assert len(response.json['member_ids']) == 2
            when('Already added to the room', form=Update(user_id=2))
            assert status == '604 Already Added To Target'
            when('Not allowed to add this person to any room',
                 form=Update(user_id=3)
                 )
            assert status == '602 Not Allowed To Add This Person To Any Room'
            when('Blocked by the user', form=Update(user_id=4))
            assert status == '601 Blocked By Target User'
        self.logout()
        self.login(
            'block@example.com',
            '123456',
            '/apiv1/tokens',
            'CREATE'
        )
        with self.given(
            'Add to  a room',
            '/apiv1/rooms/1',
            'ADD',
            form=dict(user_id=5),
        ):
            assert status == '601 Blocked By Target User'

