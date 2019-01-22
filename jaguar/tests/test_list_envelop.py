from bddrest.authoring import when, Update, status, response

from jaguar.models import Envelop, Room, Member
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestEnvelop(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.envelop1 = Envelop(body='This is envelop 1')

        cls.envelop2 = Envelop(body='This is envelop 2')

        cls.envelop3 = Envelop(body='This is envelop 3')

        cls.envelop4 = Envelop(body='This is envelop 4')

        user1 = Member(
                email='user1@example.com',
                title='user',
                access_token='access token1',
                reference_id=2,
                messages=[cls.envelop1, cls.envelop2, cls.envelop3, cls.envelop4]
            )

        room1 = Room(
            title='room1',
            members=[user1],
            messages=[cls.envelop1, cls.envelop2, cls.envelop3, cls.envelop4]
        )
        session.add(room1)
        session.commit()

    def test_list(self):
        self.login('user1@example.com')

        with cas_mockup_server(), self.given(
            'List envelops',
            '/apiv1/envelops',
            'LIST',
        ):
            assert status == 200
            assert len(response.json) == 4

#            when('Sort envelops', query=dict(sort='body'))
#            assert response.json[0]['body'] == self.envelop1.body
#
#            when(
#                'Reverse sorting body content by alphabet',
#                query=dict(sort='-body')
#            )
#            assert response.json[0]['body'] == self.envelop4.body

            import pudb; pudb.set_trace()  # XXX BREAKPOINT
            when(
                'Filter envelops',
                query=dict(sort='id', body=self.envelop1.body)
            )
            assert response.json[0]['body'] == self.envelop1.body

#            when(
#                'List projects except one of them',
#                query=dict(sort='id', title='!My awesome project')
#            )
#            assert response.json[0]['title'] == 'My first project'
#
#            when(
#                'List projects with filtering by status',
#                query=dict(sort='id', status='active')
#            )
#            assert response.json[0]['status'] == 'active'
#
#            when(
#                'List projects excepts one of statuses',
#                query=dict(sort='id', status='!active')
#            )
#            assert response.json[0]['status'] == 'on-hold'

#            with self.given(
#                'Project pagination',
#                '/apiv1/projects',
#                'LIST',
#                query=dict(sort='id', take=1, skip=2)
#            ):
#                assert response.json[0]['title'] == 'My third project'
#
#                when(
#                    'Manipulate sorting and pagination',
#                    query=dict(sort='-title', take=1, skip=2)
#                )
#                assert response.json[0]['title'] == 'My first project'
#
#                when('Request is not authorized', authorization=None)
#                assert status == 401
#
