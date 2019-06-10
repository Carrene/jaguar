from bddrest.authoring import status, response, when, given
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
            name='user1_name',
            access_token='access token1',
            reference_id=2,
            messages=[cls.message1, cls.message2]
        )
        cls.user2 = Member(
            email='user2@example.com',
            title='user 2',
            name='user2_name',
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
            assert response.json[0]['body'] == self.message1.body

            when('Search without query parameter', form=given - 'query')
            assert status == '715 Form Query Or Query String Is Required'

            when(
                'Search string must be less than 20 charecters',
                form=given | dict(query=(50 + 1) * 'a')
            )
            assert status == '702 Must Be Less Than 50 Characters'

            when(
                'Try to sort the response',
                query=dict(sort='id'),
                form=given | dict(query='message')
            )
            assert len(response.json) == 3
            assert response.json[0]['id'] < response.json[1]['id']

            when(
                'Trying ro sort the response in descend ordering',
                query=dict(sort='-id'),
                form=given | dict(query='message')
            )
            assert len(response.json) == 3
            assert response.json[0]['id'] > response.json[1]['id']

            when(
                'Filtering the response',
                query=dict(id=self.message1.id)
            )
            assert len(response.json) == 1
            assert response.json[0]['id'] == self.message1.id

            when(
                'Trying to filter the response ignoring the title',
                query=dict(title=f'!{self.message1.id}'),
                form=given | dict(query='message')
            )
            assert len(response.json) == 3

            when(
                'Testing pagination',
                query=dict(take=1, skip=1),
                form=given | dict(query='message')
            )
            assert len(response.json) == 1

            when(
                'Sort before pagination',
                query=dict(sort='-id', take=2, skip=1),
                form=given | dict(query='message')
            )
            assert len(response.json) == 2
            assert response.json[0]['id'] > response.json[1]['id']

    def test_request_with_query_string(self):
        self.login(self.user1.email)

        with cas_mockup_server(), self.given(
            'Test request using query string',
            f'/apiv1/targets/id: {self.room1.id}/messages',
            'SEARCH',
            query=dict(query='Sec')
        ):
            assert status == 200
            assert len(response.json) == 1

            when('An unauthorized search', authorization=None)
            assert status == 401

