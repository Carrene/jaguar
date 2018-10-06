
from bddrest.authoring import response, when, Update, Remove, status

from jaguar.models.membership import User
from jaguar.models.target import Room
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestListRooms(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.user1 = User(
            email='user1@example.com',
            title='user1',
            access_token='access token1',
            reference_id=2
        )
        user2 = User(
            email='user2@example.com',
            title='user2',
            access_token='access token2',
            reference_id=3
        )
        user1_room1 = Room(title='room1', owner=cls.user1)
        user2_room1 = Room(title='room1', owner=user2)
        session.add_all([user1_room1, user2_room1])
        session.commit()

    def test_list_rooms_of_user(self):
         self.login('user1@example.com')

         with cas_mockup_server(), self.given(
             'List all the rooms a user owns',
             '/apiv1/rooms',
             'LIST',
         ):
             assert status == 200
             assert len(response.json) == 1
             assert response.json[0]['title'] == 'room1'
             assert response.json[0]['ownerId'] == self.user1.id

