from bddrest.authoring import given, when, Update, status, response

from jaguar.tests.helpers import AutoDocumentationBDDTest
from jaguar.models import Room, User, Message


class TestListMessages(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user1 = User(
            email='user1@example.com',
            password='123456',
            title='user',
        )
        user2 = User(
            email='user2@example.com',
            password='123456',
            title='user2'
        )
        room1 = Room(title='room1', type='room')
        room2 = Room(title='room2', type='room')
        room1.members.append(user1)
        message1 = Message(body='This is message 1', mime_type='text/plain')
        message2 = Message(body='This is message 2', mime_type='text/plain')
        message3 = Message(body='This is message 3', mime_type='test/plain')
        session.add_all([room1, room2])
        session.add(user2)
        session.flush()
        message1.sender_id = user1.id
        message3.sender_id = user1.id
        message1.target_id = room1.id
        message3.target_id = room1.id
        message2.sender_id = user1.id
        message2.target_id = room2.id
        session.add_all([message1, message2, message3])
        session.commit()

    def test_list_messages_of_target(self):
        self.login(
            email='user1@example.com',
            password='123456',
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'List messages of a target',
            '/apiv1/targets/id:1/messages',
            'LIST',
        ):
            assert status == 200
            assert len(response.json) == 2

    def test_sorting(self):
        self.login(
            email='user1@example.com',
            password='123456',
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'Sorting the response',
            '/apiv1/targets/id:1/messages',
            'LIST',
            query=dict(sort='id')
        ):
            assert len(response.json) == 2
            assert response.json[0]['body'] == 'This is message 1'

            when('Sorting the response descending', query=Update(sort='-id'))
            assert response.json[0]['body'] == 'This is message 3'

    def test_pagination(self):
        self.login(
            email='user1@example.com',
            password='123456',
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'Testing pagination',
            '/apiv1/targets/id:1/messages',
            'LIST',
            query=dict(take=1, skip=1)
        ):
            assert len(response.json) == 1
            assert response.json[0]['body'] == 'This is message 3'

            when(
                'Sorting befor pagination',
                query=dict(sort='-id', take=1, skip=1)
            )
            assert response.json[0]['body'] == 'This is message 1'

    def test_filtering(self):
        self.login(
            email='user1@example.com',
            password='123456',
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'Filtering the response',
            '/apiv1/targets/id:1/messages',
            'LIST',
            query=dict(id=1)
        ):
            assert len(response.json) == 1

            when('Try to pass an Unauthorized request', authorization=None)
            assert status == 401

    def test_Forbidden_request(self):

        self.login(
            email='user2@example.com',
            password='123456',
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'Not member tries to list messages of a target',
            '/apiv1/targets/id:1/messages',
            'LIST',
        ):
            assert status == 403

