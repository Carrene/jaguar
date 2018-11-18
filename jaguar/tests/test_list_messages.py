from os.path import abspath, join, dirname

from bddrest.authoring import when, Update, status, response

from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server
from jaguar.models import Room, Member, Message
from sqlalchemy_media import StoreManager


this_dir = abspath(join(dirname(__file__)))
image_path = join(this_dir, 'stuff', '150x150.png')


class TestListMessages(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        with StoreManager(session):
            message1 = Message(
                body='This is message 1',
                mimetype='text/plain',
            )
            message2 = Message(
                body='This is message 2',
                mimetype='text/plain',
            )
            message3 = Message(
                body='This is message 3',
                mimetype='text/plain',
            )
            message4 = Message(
                body='This is message 4',
                mimetype='text/plain',
            )
            message5 = Message(
                body='This is message 5',
                mimetype='image/png',
                attachment=image_path
            )
            user1 = Member(
                email='user1@example.com',
                title='user',
                access_token='access token1',
                reference_id=2,
                messages=[message1, message2, message3, message5]
            )
            user2 = Member(
                email='user2@example.com',
                title='user2',
                access_token='access token2',
                reference_id=3
            )
            session.add(user2)
            user3 = Member(
                email='user3@example.com',
                title='user3',
                access_token='access token3',
                reference_id=4,
                messages=[message4]
            )
            room1 = Room(
                title='room1',
                type='room',
                members=[user1, user3],
                messages=[message1, message3, message4, message5]
            )
            session.add(room1)
            room2 = Room(title='room2', type='room', messages=[message2])
            session.add(room2)
            session.commit()

    def test_list_messages_of_target(self):
        self.login('user1@example.com')

        with cas_mockup_server(), self.given(
            'List messages of a target',
            '/apiv1/targets/id:1/messages',
            'LIST',
        ):
            assert status == 200
            assert len(response.json) == 4
            assert response.json[0]['body'] == 'This is message 1'
            assert response.json[0]['isMine'] is True

            assert response.json[2]['body'] == 'This is message 4'
            assert response.json[2]['isMine'] is False

            when(
                'Try to send form in the request',
                form=dict(parameter='parameter')
            )
            assert status == '711 Form Not Allowed'

    def test_sorting(self):
        self.login('user1@example.com')

        with cas_mockup_server(), self.given(
            'Sorting the response',
            '/apiv1/targets/id:1/messages',
            'LIST',
            query=dict(sort='id')
        ):
            assert len(response.json) == 4
            assert response.json[0]['body'] == 'This is message 1'

            when('Sorting the response descending', query=Update(sort='-id'))
            assert response.json[0]['body'] == 'This is message 5'

    def test_pagination(self):
        self.login('user1@example.com')

        with cas_mockup_server(), self.given(
            'Testing pagination',
            '/apiv1/targets/id:1/messages',
            'LIST',
            query=dict(take=1, skip=1)
        ):
            assert len(response.json) == 1
            assert response.json[0]['body'] == 'This is message 3'

            when(
                'Sorting befor pagination',
                query=dict(sort='-id', take=2, skip=1)
            )
            assert len(response.json) == 2
            assert response.json[0]['body'] == 'This is message 4'

    def test_filtering(self):
        self.login('user1@example.com')

        with cas_mockup_server(), self.given(
            'Filtering the response',
            '/apiv1/targets/id:1/messages',
            'LIST',
            query=dict(id=1)
        ):
            assert len(response.json) == 1

            when('Try to pass an Unauthorized request', authorization=None)
            assert status == 401

    def test_forbidden_request(self):
        self.login('user2@example.com')

        with cas_mockup_server(), self.given(
            'Not member tries to list messages of a target',
            '/apiv1/targets/id:1/messages',
            'LIST',
        ):
            assert status == 403

