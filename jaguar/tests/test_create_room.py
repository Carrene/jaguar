
from bddrest.authoring import response, when, Remove, Update
from restfulpy.orm import DBSession

from jaguar.models.membership import User

from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestRoom(AutoDocumentationBDDTest):

    def test_create_room(self):
        with self.given(
            'Create a room',
            url='/apiv1/rooms',
            verb='CREATE',
            form=dict(title='example')
        ):

            assert response.status == '200 OK'
