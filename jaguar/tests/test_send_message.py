from bddrest.authoring import given, when, Update, status, response

from jaguar.tests.helpers import AutoDocumentationBDDTest
from jaguar.models import User, Room, Direct


class TestSendMessage(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user1 = User(
            email='user1@example.com',
            password='123456',
            title='user1',
        )
        blocker = User(
            email='blocker@example.com',
            password='123456',
            title='blocker'
        )
        blocker.blocked_users.append(user1)
        room = Room(title='example')
        direct = Direct(title='direct')
        session.add(blocker)
        session.add(room)
        session.add(direct)
        session.commit()

    def test_send_message_to_target(self):
        self.login(
            email='user1@example.com',
            password='123456',
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'Send a message to a target',
            '/apiv1/targets/id:1/messages',
            'SEND',
            form=dict(body='hello world!', type='text/plain')
        ):
            assert status == 200
            assert response.json['body'] == 'hello world!'

            when('Invalid target id', url_parameters=Update('Invalid'))
            assert status == '706 Ivalid Target Id'



