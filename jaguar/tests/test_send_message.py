from bddrest.authoring import given, when, Update, status, response, Remove

from jaguar.tests.helpers import AutoDocumentationBDDTest
from jaguar.models import User, Room, Direct


class TestSendMessage(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user1 = User(
            email='user1@example.com',
            title='user1',
            access_token='access token'
        )
        room = Room(title='example', type='room')
        direct = Direct(title='direct', type='direct')
        session.add(user1)
        session.add(room)
        session.commit()

    def test_send_message_to_target(self):
        self.login('user1@example.com')

        with self.given(
            'Send a message to a target',
            '/apiv1/targets/id:1/messages',
            'SEND',
            form=dict(body='hello world!', mimeType='text/plain')
        ):
            assert status == 200
            assert response.json['body'] == 'hello world!'

            when('Invalid target id', url_parameters=Update(id='Invalid'))
            assert status == '706 Invalid Target Id'

            when('Target does not exist', url_parameters=Update(id=3))
            assert status == '614 Target Not Exist'

            when(
                'Try to send unsopported media type',
                form=Update(mimeType='video/3gpp')
            )
            assert status == 415

            when(
                'Try to send long text',
                form=Update(body=(1024 + 1) * 'a')
            )
            assert status == '702 Must be less than 1024 charecters'

            when('Remove body from the form', form=Remove('body'))
            assert status == 400

            when('Try to pass an unauthorized request', authorization=None)
            assert status == 401

