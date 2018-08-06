from bddrest.authoring import given, when, status, Update, response

from jaguar.models import User
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestSearchUser(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user1 = User(
            email='user1@example.com',
            password='123456',
            title='user1',
            username='user1',
        )
        user2 = User(
            email='user2@gmail.com',
            password='123456',
            title='user2',
            username='user2',
        )
        session.add_all([user1, user2])
        session.commit()

    def test_search_user(self):
        with self.given(
            'Search for a user',
            '/apiv1/users',
            'SEARCH',
            form=dict(query='Use'),
        ):
            assert status == 200
            assert response.json[0]['title'] == 'user1'
            assert len(response.json) == 2

            when('Search using email', form=Update(query='exam'))
            assert status == 200
            assert len(response.json) == 1

            when(
                'Trying to pass search non existing user',
                form=Update(query='sample')
            )
            assert status == '611 User Not Found'

            when(
                'Search string must be less than 20 charecters',
                form=Update(
                    query= \
                    'The search string should be less than 20 charecters'
                )
            )
            assert status == '702 Must Be Less Than 20 Charecters'

    def test_sorting(self):
        with self.given(
            'Test sorting',
            '/apiv1/users',
            'SEARCH',
            form=dict(query='user'),
            query=('sort=title'),
        ):
            assert response.json[0]['id'] == 1

            when(
                'Trying ro sort the response in descend ordering',
                 query=('sort=-title')
            )
            assert response.json[0]['id'] == 2

    def test_filtering(self):
        with self.given(
            'Test filtering',
            '/apiv1/users',
            'SEARCH',
            form=dict(query='user'),
            query=('title=user2'),
        ):
            assert len(response.json) == 1
            assert response.json[0]['title'] == 'user2'

            when(
                'Trying to filter the response ignoring the title',
                 query=('title!=user2')
            )
            assert response.json[0]['title'] != 'user2'

    def test_pagination(self):
        with self.given(
            'Test pagination',
            '/apiv1/users',
            'SEARCH',
            form=dict(query='user'),
            query=('take=1&skip=1')
        ):
            assert len(response.json) == 1
            assert response.json[0]['title'] == 'user2'

            when('Sort before pagination', query=('sort=-id&take=3&skip=1'))
            assert len(response.json) == 1
            assert response.json[0]['title'] == 'user1'

    def test_request_with_query_string(self):
        with self.given(
            'Test request using query string',
            '/apiv1/users',
            'SEARCH',
            query=dict(query='user')
        ):
            assert status == 200
            assert len(response.json) == 2

