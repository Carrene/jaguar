
from restfulpy.orm import DBSession
from restfulpy.principal import JwtPrincipal, JwtRefreshToken
from nanohttp import context
from bddrest.authoring import response, when, Update, Remove, status

from jaguar.models.membership import User
from jaguar.models.target import Room
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestRoom(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user = User(
            email='already.added@example.com',
            title='example',
            password='123456',
        )
        user.is_active = True

        room_member = User(
            email='member@example.com',
            title='member',
            password='123456',
        )

        never_add_to_room = User(
            email='never.add@example.com',
            title='never',
            password='123456',
            add_to_room = False,
        )

        room = Room(title='example', type='room')
        room.members.append(room_member)
        session.add_all([user, room, never_add_to_room])
        session.commit()

    def test_create_room(self):
        self.login(
            email='already.added@example.com',
            password='123456',
            url='/apiv1/tokens',
            verb='CREATE'
        )
        with self.given(
            'Creating a room',
            url='/apiv1/rooms/1',
            verb='ADD',
            form=dict(user_id=1),
        ):

            assert status == 200
            assert len(response.json['member_ids']) == 2

            when('Already added to the room', form=Update(user_id=2))
            assert status == '604 Already Added To Target'

            when('Not allowed to add to any room',
                 form=Update(user_id=3)
            )
            assert status == 602


