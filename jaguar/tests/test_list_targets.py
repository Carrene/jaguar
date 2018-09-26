
from bddrest.authoring import response, when, Update, Remove, status

from jaguar.models.membership import User
from jaguar.models.target import Room, Direct
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestListTarget(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user1 = User(
            email='user1@example.com',
            title='user1',
            access_token='access token',
        )
        user2 = User(
            email='user2@example.com',
            title='user2',
            access_token='access token',
        )
        user1_room1 = Room(title='room1', owner=user1)
        user2_room1 = Room(title='room1', owner=user2)
        session.add_all([user1_room1, user2_room1])
        session.commit()

    def test_list_targets_of_user(self):
         self.login('user1@example.com')

         with self.given(
             'List targets of a user',
             '/apiv1/targets',
             'LIST',
         ):
             assert status == 200
             assert len(response.json) == 1
             assert response.json[0]['title'] == 'room1'

