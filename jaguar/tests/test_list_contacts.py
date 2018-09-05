
from bddrest.authoring import response, when, Update, status

from jaguar.models.membership import User
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestListContact(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user = User(
            email='user@example.com',
            title='user',
            access_token='access token',
        )
        contact1 = User(
            email='contact1@example.com',
            title='contact1',
            access_token='access token',
        )
        contact2 = User(
            email='contact2@example.com',
            title='contact2',
            access_token='access token',
        )

        # This contact is added to make sure the query works correctly
        contact3 = User(
            email='contact3@example.com',
            title='contact3',
            access_token='access token',
            show_email=True,
        )
        user.contacts = [contact1, contact2]
        contact1.contacts.append(contact3)
        session.add(user)
        session.commit()

    def test_list_contacts(self):
        self.login(
            dict(email='user@example.com'),
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'List a user contacts',
            '/apiv1/contacts',
            'LIST',
        ):
            assert status == 200
            assert len(response.json) == 2

    def test_sorting(self):
        self.login(
            dict(email='user@example.com'),
            url='/apiv1/tokens',
            verb='CREATE',
        )

        with self.given(
            'Try to sort the response',
            '/apiv1/contacts',
            'LIST',
            query=dict(sort='title')
        ):
            assert response.json[0]['title'] == 'contact1'

            when(
                'Try to sort the response in descending order',
                query=dict(sort='-title')
            )
            assert response.json[0]['title'] == 'contact2'

    def test_filtering(self):
        self.login(
            dict(email='user@example.com'),
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'Filtering the response using title',
            '/apiv1/contacts',
            'LIST',
            query=dict(title='contact2')
        ):
            assert len(response.json) == 1
            assert response.json[0]['title'] == 'contact2'

            when(
                'Try to filter the response ignoring a title',
                query=dict(title='!contact2')
            )
            assert len(response.json) == 1
            assert response.json[0]['title'] != 'contact2'

    def test_pagination(self):
        self.login(
            dict(email='user@example.com'),
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'Testing pagination',
            '/apiv1/contacts',
            'LIST',
            query=dict(take=1, skip=1)
        ):
            assert response.json[0]['title'] == 'contact2'

            when(
                'Test sorting before pagination',
                query=dict(sort='-title', take=1, skip=1)
            )
            assert response.json[0]['title'] == 'contact1'

            when('An unauthorized request', authorization=None)
            assert status == 401

