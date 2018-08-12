from restfulpy.orm import DBSession
from restfulpy.principal import JwtPrincipal, JwtRefreshToken
from nanohttp import context
from bddrest.authoring import response, when, Update, Remove, status

from jaguar.models.membership import User
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestRoom(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user = User(
            email='user@example.com',
            title='user',
            password='123456',
        )
        session.add(user)
        session.commit()

    def test_create_room(self):
        self.login(
            'user@example.com',
            '123456',
            '/apiv1/tokens',
            'CREATE'
        )
        with self.given(
            'Creating a room',
            '/apiv1/rooms',
            'CREATE',
            form=dict(title='example'),
        ):
            assert status == 200
            assert response.json['title'] == 'example'
            assert response.json['ownerId'] == 1
            assert len(response.json['administratorIds']) == 1
            assert len(response.json['memberIds']) == 1

            when(
                'The room title is less than minimum',
                form=Update(title='min')
            )
            assert status == '701 Must Be Greater Than 4 Charecters'

            when(
                'The Room Title Is Less Than Minimum',
                form=Update(
                    title='The room title should not be more than 32 charecters'
                )
            )
            assert status == '702 Must Be Less Than 32 Charecters'

            when('Title is required', form=Remove('title'))
            assert status == '703 Room Title Is Required'

