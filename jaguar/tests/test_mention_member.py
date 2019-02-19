from bddrest.authoring import status, when, given, response

from jaguar.models import Member, Direct
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestMention(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.member1 = Member(
            email='user1@example.com',
            title='user1',
            access_token='access token1',
            reference_id=2
        )
        cls.member2 = Member(
            email='user2@example.com',
            title='user2',
            access_token='access token2',
            reference_id=3
        )
        cls.member3 = Member(
            email='user3@example.com',
            title='user3',
            access_token='access token3',
            reference_id=4
        )
        session.add(cls.member3)

        direct1 = Direct(
            members=[cls.member1, cls.member2]
        )
        session.add(direct1)

        direct2 = Direct(
            members=[cls.member1, cls.member3]
        )
        session.add(direct2)
        session.commit()

    def test_mention(self):
        self.login(self.member1.email)

        with cas_mockup_server(), self.given(
            'Mention a target',
            f'/apiv1/members/member_id:{self.member2.id}/mentions',
            'MENTION',
            form=dict(body='abc')
        ):
            assert status == 200
            assert response.json['body'] == 'abc'

            when(
                'Body length is more than limit',
                form=given | dict(body=(65536 + 1) * 'a')
            )
            assert status == '702 Must be less than 65536 charecters'

            when(
                'There is no direct between mentioned and mentioner member',
                url_parameters=dict(member_id=self.member3.id)
            )
            assert response.json['body'] == 'abc'

            when('User is logged out', authorization=None)
            assert status == 401

