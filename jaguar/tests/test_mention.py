from bddrest.authoring import status, when, given, response

from jaguar.models import Member, Room
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestMention(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        member1 = Member(
            email='user1@example.com',
            title='user1',
            access_token='access token1',
            reference_id=2
        )
        cls.room = Room(
            title='example',
            members=[member1]
        )
        session.add(cls.room)
        session.commit()

    def test_mention(self):
        self.login('user1@example.com')

        with cas_mockup_server(), self.given(
            'Mention a target',
            f'/apiv1/targets/{self.room.id}/mentions',
            'MENTION',
            form=dict(reference='abc', body='def')
        ):
            assert status == 200
            assert response.json['reference'] == 'abc'
            assert response.json['body'] == 'def'

            when(
                'Reference lenght is more than limit',
                form=given | dict(reference=(512 + 1) * 'a')
            )
            assert status == '715 At Most 512 Characters Valid For Reference'

            when(
                'Body length is more than limit',
                form=given | dict(body=(1024 + 1) * 'a')
            )
            assert status == '702 Must be less than 1024 charecters'

            when('Remove body from the form', form=given - 'body')
            assert status == 400

            when('User is logged out', authorization=None)
            assert status == 401

