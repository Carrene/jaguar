from bddrest.authoring import status, when, given

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
            form=dict(reference='abc')
        ):
            assert status == 200

            when(
                'Reference lenght is more than limit',
                form=given | dict(reference=(512 + 1) * 'a')
            )
            assert status == 715

