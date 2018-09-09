
from bddrest.authoring import response, when, Update, Remove, status

from jaguar.models.membership import User
from jaguar.models.target import Room, Direct
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestListTarget(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user = User(
            email='user@example.com',
            title='user',
            access_token='access token',
        )
        room1 = Room(title='room1')
        direct = Direct(title='direct')
        room2 = Room(title='room2')
        room1.members.append(user)
        direct.members.append(user)
        session.add_all([direct, room1, room2])
        session.commit()

    def test_list_targets_of_user(self):
         self.login('user@example.com')

         with self.given(
             'List targets of a user',
             '/apiv1/targets',
             'LIST',
         ):
             assert status == 200
             assert len(response.json) == 2

