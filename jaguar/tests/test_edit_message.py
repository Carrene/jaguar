from bddrest.authoring import when, status, response, Update

from jaguar.models import Member, Room, Message
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestEditMessage(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        cls.session = cls.create_session()
        message1 = Message(
            body='This is message 1',
            mimetype='text/plain',
        )
        message2 = Message(
            body='This is message 2',
            mimetype='text/plain',
        )
        cls.message3 = Message(
            body='This is message 3',
            mimetype='text/plain',
        )
        user1 = Member(
            email='user1@example.com',
            title='user1',
            access_token='access token1',
            reference_id=2,
            messages=[message1, message2, cls.message3]
        )
        user2 = Member(
            email='user2@example.com',
            title='user2',
            access_token='access token2',
            reference_id=3
        )
        room = Room(
            title='room',
            type='room',
            members=[user1],
            messages=[message1, message2, cls.message3]
        )
        cls.session.add(user2)
        cls.session.add(room)
        cls.message3.soft_delete()
        cls.session.commit()

    def test_edit_the_message(self):
        self.login('user1@example.com')

        with cas_mockup_server(), self.given(
            'Try to edit a message',
            '/apiv1/messages/id:1',
            'EDIT',
            form=dict(body='Message 1 is edited')
        ):
            assert status == 200
            assert response.json['body'] == 'Message 1 is edited'
            assert response.json['id'] == 1

            when('The message not exists', url_parameters=Update(id=4))
            assert status == '614 Message Not Found'

            when(
                'Trying to pass using invalid message id',
                url_parameters=Update(id='Invalid')
            )
            assert status == '707 Invalid MessageId'

            when(
                'Try to send long text',
                form=Update(body=(1024 + 1) * 'a')
            )
            assert status == '702 Must be less than 1024 charecters'

            when(
                'Try to edit a deleted message',
                url_parameters=Update(id=self.message3.id)
            )
            assert status == 616

    # TODO: More test scenarios should be checked when other
    # Authorizations would be implemented
    def test_forbidden_request(self):
        self.login('user2@example.com')

        with cas_mockup_server(), self.given(
            'Not allowed to edit the message',
            '/apiv1/messages/id:1/',
            'EDIT',
            form=dict(body='Message 1 should not be edited'),
        ):
            assert status == 403

            when('Try to pass an unauthorized request', authorization=None)
            assert status == 401

