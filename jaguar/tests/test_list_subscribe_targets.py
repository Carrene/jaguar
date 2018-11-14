
from bddrest.authoring import response, when, Update, status

from jaguar.models.membership import Member
from jaguar.models.target import Room, Direct
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestListSubscribeTarget(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user = Member(
            email='user@example.com',
            title='user',
            access_token='access token',
            reference_id=1
        )
        user1 = Member(
            email='user1@example.com',
            title='user1',
            access_token='access token1',
            reference_id=2
        )
        user2 = Member(
            email='user2@example.com',
            title='user2',
            access_token='access token2',
            reference_id=3
        )
        session.add(user2)
        direct = Direct(members=[user, user1])
        room1 = Room(title='room1', members=[user])
        room2 = Room(title='room2', members=[user1])
        room3 = Room(title='room3', members=[user, user1])
        session.add_all([direct, room1, room2, room3])
        session.commit()

    def test_list_subscribe_target(self):
        self.login('user@example.com')

        with cas_mockup_server(), self.given(
            'List targets a user subscribe to',
            '/apiv1/subscribetargets',
            'LIST',
        ):
            assert status == 200
            assert len(response.json) == 3

    def test_sorting(self):
        self.login('user@example.com')

        with cas_mockup_server(), self.given(
            'Sorting the response',
            '/apiv1/subscribetargets',
            'LIST',
            query=dict(sort='title')
        ):
            assert len(response.json) == 3
            assert response.json[0]['type'] == 'direct'

            when(
                'Sorting the response descending',
                query=Update(sort='-title')
            )
            assert response.json[0]['type'] == 'direct'
            assert response.json[1]['type'] == 'room'
            assert response.json[1]['title'] == 'room1'
            assert response.json[2]['type'] == 'room'
            assert response.json[2]['title'] == 'room3'

    def test_pagination(self):
        self.login('user@example.com')

        with cas_mockup_server(), self.given(
            'Testing pagination',
            '/apiv1/subscribetargets',
            'LIST',
            query=dict(sort='id', take=1, skip=1)
        ):
            assert len(response.json) == 1
            assert response.json[0]['title'] == 'room1'

            when(
                'Sorting befor pagination',
                query=dict(sort='-id', take=1, skip=1)
            )
            assert len(response.json) == 1
            assert response.json[0]['title'] == 'room1'

    def test_filtering(self):
        self.login('user1@example.com')

        with cas_mockup_server(), self.given(
            'Filtering the response',
            '/apiv1/subscribetargets',
            'LIST',
            query=dict(id=1)
        ):
            assert len(response.json) == 1

            when('Try to pass an Unauthorized request', authorization=None)
            assert status == 401

