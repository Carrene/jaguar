from jaguar.tests.helpers import AutoDocumentationBDDTest
from jaguar.models import User
from bddrest.authoring import given, when, status, Update, response


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

    def test_search_for_user(self):
        with self.given(
            'Search for a user',
            '/apiv1/users',
            'SEARCH',
            form=dict(searchString='Use'),
        ):
            assert status == 200
            assert response.json[0]['title'] == 'user1'
            assert len(response.json) == 2

            when('Search in email', form=Update(searchString='exam'))
            assert status == 200
            assert len(response.json) == 1

            when(
                'Search non existing user',
                form=Update(searchString='sample')
            )
            assert status == '611 User Not Found'

            when(
                'Search string must be less than 20 charecters',
                form=Update(
                    searchString= \
                    'The search string should be less than 20 charecters'))
            assert status == '702 Must Be Less Than 20 Charecters'

    def test_sorting(self):
        with self.given(
            'Test sorting',
            '/apiv1/users',
            'SEARCH',
            form=dict(searchString='user'),
            query=('sort=title'),
        ):
            assert response.json[0]['id'] == 1

            when('Test ordering, descending sort', query=('sort=-title'))
            assert response.json[0]['id'] == 2

    def test_filtering(self):
        with self.given(
            'Test filtering',
            '/apiv1/users',
            'SEARCH',
            form=dict(searchString='user'),
            query=('title=user2'),
        ):
            assert len(response.json) == 1
            assert response.json[0]['title'] == 'user2'

            when('Test filtering with two parameter', query=('title!=user2'))
            assert response.json[0]['title'] != 'user2'

    def test_pagination(self):
        with self.given(
            'Test pagination',
            '/apiv1/users',
            'SEARCH',
            form=dict(searchString='user'),
            query=('take=1&skip=1')
        ):
            assert len(response.json) == 1
            assert response.json[0]['title'] == 'user2'

            when('Sort before pagination', query=('sort=-id&take=3&skip=1'))
            assert len(response.json) == 1
            assert response.json[0]['title'] == 'user1'

    def test_rquest_with_query_string(self):
        with self.given(
            'Test if request works with query string',
            '/apiv1/users',
            'SEARCH',
            query=dict(searchString='user')
        ):
            assert status == 200
            assert len(response.json) == 2

