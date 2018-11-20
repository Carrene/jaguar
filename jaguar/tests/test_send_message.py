from bddrest.authoring import given, when, Update, status, response, Remove

from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server
from jaguar.models import Member, Room, Direct


class TestSendMessage(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
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
        room = Room(
            title='example',
            members=[user1]
        )
        direct = Direct()
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
            assert response.json['isMine'] is True

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

            self.logout()
            self.login('user2@example.com')

            when(
                'Not member try to send a message',
                 authorization=self._authentication_token
            )
            assert status == 403

