
from bddrest.authoring import response, when, Remove, Update
from restfulpy.application import Application
from restfulpy.orm import DBSession
from restfulpy.testing import ApplicableTestCase

from ..controllers.root import Root
from jaguar.authentication import Authenticator
from jaguar.models.membership import User


class TestRoom(ApplicableTestCase):
    __application__ = Application(
        'Mockup',
        root=Root(),
        authenticator=Authenticator()
    )

    def test_create_room(self):
        with self.given(
            'Create a room',
            url='/apiv1/rooms',
            verb='CREATE',
            form=dict(title='example')
        ):

            assert response.status == '200 OK'

