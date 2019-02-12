import io
from os.path import abspath, join, dirname

from bddrest.authoring import when, status, response
from sqlalchemy_media import StoreManager

from jaguar.models import Member, Room, Message, MemberMessage
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


THIS_DIR = abspath(join(dirname(__file__)))
IMAGE_PATH = join(THIS_DIR, 'stuff', '150x150.png')


class TestSeeMessage(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        with StoreManager(session):
            with open(IMAGE_PATH, 'rb') as f:
                cls.user = Member(
                    email='user@example.com',
                    title='user',
                    access_token='access token',
                    reference_id=1,
                )
                session.add(cls.user)

                room = Room(
                    title='room',
                    type='room',
                    members=[cls.user]
                )
                session.add(room)
                session.flush()

                cls.message1 = Message(
                    body='This is message 1',
                    mimetype='text/plain',
                    target_id=room.id,
                    sender_id=cls.user.id,
                )
                session.add(cls.message1)

                cls.message2 = Message(
                    body='This is message 2',
                    mimetype='text/plain',
                    target_id=room.id,
                    sender_id=cls.user.id
                )
                session.add(cls.message2)

                cls.message3 = Message(
                    body='This is message 3',
                    mimetype='text/plain',
                    target_id=room.id,
                    sender_id=cls.user.id,
                    attachment=io.BytesIO(f.read()),
                )
                session.add(cls.message3)
                session.flush()

                member_message1 = MemberMessage(
                    member_id=cls.user.id,
                    message_id=cls.message1.id
                )
                session.add(member_message1)

                member_message2 = MemberMessage(
                    member_id=cls.user.id,
                    message_id=cls.message2.id
                )
                session.add(member_message2)
                session.commit()

    def test_see_message(self):
        self.login(self.user.email)

        with cas_mockup_server(), self.given(
            f'See a message',
            f'/apiv1/messages/id:{self.message3.id}',
            f'SEE'
        ):
            assert status == 200
            assert response.json['id'] == self.message3.id
            assert response.json['body'] == self.message3.body
            assert response.json['seenAt'] is not None
            assert response.json['attachment'] is not None
            assert response.json['modifiedAt'] is None

            when('Trying to pass with message already seen')
            assert status == '619 Message Already Seen'

            when('Message is not found', url_parameters=dict(id=0))
            assert status == 404

            when(
                'Message is not found with alphabetical id',
                url_parameters=dict(id='Alphabetical')
            )
            assert status == 404

            when('Try to pass unauthorize request', authorization=None)
            assert status == 401

