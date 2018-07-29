
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
            assert response.json['title'] == 'example'
            when(
                'The room title is less than minimum',
                form=Update(title='min')
            )
            assert response.status ==\
                '701 Must Be Greater Than 4 Charecters'

            when(
                'The Room Title Is Less Than Minimum',
                form=\
                Update(
                    title=\
                    'The room title should not be more than 32 charecters')
            )
            assert response.status == '702 Must Be Less Than 32 Charecters'
            when(
                'title is required',
                form = Remove('title')
            )
            assert response.status == '703 Room Title Is Required'

