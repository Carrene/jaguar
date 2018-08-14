from bddrest.authoring import given, when, Update, status

from jaguar.tests.helpers import AutoDocumentationBDDTest
from jaguar.models import User, Room


class TestSendMessage(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user1 = User(
            email='user1@example.com',
            password='123456',
            title='user1',
        )
        room = Room(title='example')
        session.add(user1)
        session.add(room)
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

