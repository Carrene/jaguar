
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
        room = Room(title='example', type='room')
        session.add_all([user, room])
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
