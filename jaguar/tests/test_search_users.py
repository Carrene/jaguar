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
            form=dict(search_string='Use'),
        ):
            assert status == 200
            assert response.json[0]['title'] == 'user1'
            assert len(response.json) == 2

            when('Search in email', form=Update(search_string='exam'))
            assert status == 200
            assert len(response.json) == 1

            when(
                'Search non existing user',
                form=Update(search_string='sample')
            )
            assert status == '611 User Not Found'

            when(
                'Search string must be less than 20 charecters',
                form=Update(
                    search_string= \
                    'The search string should be less than 20 charecters'
                )
            )
            assert status == '702 Must Be Less Than 20 Charecters'

