from bddrest.authoring import status, response
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server

from jaguar.models import Member, Message, Room


class TestMessage(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.message1 = Message(
            body='First message',
            mimetype='text/plain',
        )
        cls.message2 = Message(
            body='Second message',
            mimetype='text/plain',
        )
        cls.message3 = Message(
            body='Third message',
            mimetype='text/plain',
        )
        cls.user1 = Member(
            email='user1@example.com',
            title='user 1',
            access_token='access token1',
            reference_id=2,
            messages=[cls.message1, cls.message2]
        )
        cls.user2 = Member(
            email='user2@example.com',
            title='user 2',
            access_token='access token2',
            reference_id=3,
            messages=[cls.message3]
        )
        cls.room1 = Room(
            title='room1',
            type='room',
            members=[cls.user1, cls.user2],
            messages=[cls.message3, cls.message1, cls.message2]
        )
        session.add(cls.room1)
        session.commit()

    def test_search_message(self):
        self.login(self.user1.email)

        with cas_mockup_server(), self.given(
            'Search for a message by submitting form',
            f'/apiv1/targets/id: {self.room1.id}/messages',
            'SEARCH',
            form=dict(query='Fir'),
        ):
            assert status == 200
            assert len(response.json) == 1
            assert response.json[0]['title'] == self.issue1.title

#            when('Search without query parameter', form=given - 'query')
#            assert status == '912 Query Parameter Not In Form Or Query String'
#
#            when(
#                'Search string must be less than 20 charecters',
#                form=given | dict(query=(50 + 1) * 'a')
#            )
#            assert status == '704 At Most 50 Characters Valid For Title'
#
#            when(
#                'Try to sort the response',
#                query=dict(sort='id'),
#                form=given | dict(query='issue')
#            )
#            assert len(response.json) == 4
#            assert response.json[0]['id'] < response.json[1]['id']
#
#            when(
#                'Trying ro sort the response in descend ordering',
#                query=dict(sort='-id'),
#                form=given | dict(query='issue')
#            )
#            assert len(response.json) == 4
#            assert response.json[0]['id'] > response.json[1]['id']
#
#            when('Filtering the response', query=dict(title=self.issue1.title))
#            assert len(response.json) == 1
#            assert response.json[0]['title'] == self.issue1.title
#
#            when(
#                'Trying to filter the response ignoring the title',
#                query=dict(title=f'!{self.issue1.title}'),
#                form=given | dict(query='issue')
#            )
#            assert len(response.json) == 3
#
#            when(
#                'Testing pagination',
#                query=dict(take=1, skip=1),
#                form=given | dict(query='issue')
#            )
#            assert len(response.json) == 1
#
#            when(
#                'Sort before pagination',
#                query=dict(sort='-id', take=3, skip=1),
#                form=given | dict(query='issue')
#            )
#            assert len(response.json) == 3
#            assert response.json[0]['id'] > response.json[1]['id']
#
#            when(
#                'Filtering unread issues',
#                query=dict(unread='true'),
#                form=given | dict(query='issue')
#            )
#            assert len(response.json) == 1
#            assert response.json[0]['id'] == self.issue1.id
#
#    def test_request_with_query_string(self):
#        self.login(self.member.email)
#
#        with oauth_mockup_server(), self.given(
#            'Test request using query string',
#            '/apiv1/issues',
#            'SEARCH',
#            query=dict(query='Sec')
#        ):
#            assert status == 200
#            assert len(response.json) == 1
#
#            when('An unauthorized search', authorization=None)
#            assert status == 401
#
#
