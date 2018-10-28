from bddrest.authoring import given, when, Update, status, response, Remove

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
        cls.message2 = Message(
            body='This is message 2',
            mimetype='text/plain'
        )
        user1 = User(
            email='user1@example.com',
            title='user1',
            access_token='access token1',
            reference_id=2,
            messages=[cls.message1, cls.message2]
        )
        user2 = User(
            email='user2@example.com',
            title='user2',
            access_token='access token2',
            reference_id=3
        )
        session.add(user2)
        room = Room(
            title='example',
            messages=[cls.message1, cls.message2],
            members=[user1]
        )
        direct = Direct()
        session.add(room)
        cls.message2.soft_delete()
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

            when('Try to pass an unauthorized request', authorization=None)
            assert status == 401

            when(
                'Reply a message',
                 form=Update(
                     body='A reply to message 1',
                     mimetype='text/plain',
                     replyTo=self.message1.id
                 )
            )
            assert status == 200
            assert response.json['replyTo']['body'] == self.message1.body

            when(
                'Requested message not found',
                 form=Update(
                     body='A reply to message 1',
                     mimetype='text/plain',
                     replyTo=5
                 )
            )
            assert status == '614 Message Not Found'

            when(
                'Request a message with invalid message id',
                 form=Update(
                     body='A reply to message 1',
                     mimetype='text/plain',
                     replyTo='Invalid'
                 )
            )
            assert status == '707 Invalid MessageId'

            when(
                'Requested message is already deleted',
                 form=Update(
                     body='A reply to message 1',
                     mimetype='text/plain',
                     replyTo=self.message2.id
                 )
            )
            assert status == '616 Message Already Deleted'

            self.logout()
            self.login('user2@example.com')

            when(
                'Not member try to send a message',
                 authorization=self._authentication_token
            )
            assert status == 403

