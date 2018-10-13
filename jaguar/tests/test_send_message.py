from bddrest.authoring import given, when, Update, status, response, Remove, \
    Append

from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server
from jaguar.models import User, Room, Direct, Message


class TestSendMessage(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.message1 = Message(
            body='This is message 1',
            mimetype='text/plain'
        )
        user1 = User(
            email='user1@example.com',
            title='user1',
            access_token='access token1',
            reference_id=2,
            messages=[cls.message1]
        )
        room = Room(title='example', type='room', messages=[cls.message1])
        direct = Direct(title='direct', type='direct')
        session.add(user1)
        session.add(room)
        session.commit()

    def test_send_message_to_target(self):
        self.login('user1@example.com')

        with cas_mockup_server(), self.given(
            'Send a message to a target',
            '/apiv1/targets/id:1/messages',
            'SEND',
            form=dict(body='hello world!', mimetype='text/plain')
        ):
            assert status == 200
            assert response.json['body'] == 'hello world!'
            assert response.json['isMine'] == True

            when('Invalid target id', url_parameters=Update(id='Invalid'))
            assert status == '706 Invalid Target Id'

            when('Target does not exist', url_parameters=Update(id=3))
            assert status == '614 Target Not Exist'

            when(
                'Try to send unsopported media type',
                form=Update(mimetype='video/3gpp')
            )
            assert status == 415

            when(
                'Try to send long text',
                form=Update(body=(1024 + 1) * 'a')
            )
            assert status == '702 Must be less than 1024 charecters'

            when('Remove body from the form', form=Remove('body'))
            assert status == 400

            when(
                'The message is reply to another message',
                form=Append(replyTo=self.message1.id)
            )
            assert status == 200
            assert response.json['replyRoot'] == self.message1.id
            assert response.json['replyTo']['body'] == 'This is message 1'

            when('Try to pass an unauthorized request', authorization=None)
            assert status == 401

