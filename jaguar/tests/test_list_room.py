
from restfulpy.orm import DBSession
from restfulpy.principal import JwtPrincipal, JwtRefreshToken
from nanohttp import context
from bddrest.authoring import response, when, Update, Remove, status

from jaguar.models.membership import User
from jaguar.models.target import Room
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestListTarget(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user = User(
            email='already.added@example.com',
            title='example',
            password='123456',
        )
        user.is_active = True

        room = Room(title='example')
        sample_room = Room(title='sample')
        room.members.append(user)
        sample_room.members.append(user)
        session.add_all([room, sample_room])
        session.commit()


    def test_list_targets_of_user(self):
         self.login(
             email='already.added@example.com',
             password='123456',
             url='/apiv1/tokens',
             verb='CREATE'
         )

         with self.given(
             'List targets of a user',
             url='/apiv1/targets',
             verb='LIST',
         ):

             assert status == 200
             assert len(response.json) == 2

