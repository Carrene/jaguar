from bddrest.authoring import status, given, when, Update, response

from jaguar.tests.helpers import AutoDocumentationBDDTest
from jaguar.models import User, blocked


class TestDirect(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user1 = User(
            email='user1@example.com',
            title='user1',
            access_token='access token',
        )
        user2 = User(
            email='user2@example.com',
            title='user2',
            access_token='access token',
        )
        blocker = User(
            email='blocker@example.com',
            title='blocker',
            access_token='access token',
        )
        blocker.blocked_users.append(user1)
        session.add_all([blocker, user2])
        session.commit()

    def test_creat_token(self):
        self.login('user1@example.com')

        with self.given(
            'Try to create a direct with a user',
            '/apiv1/directs',
            'CREATE',
            form=dict(userId=3)
        ):
            assert status == 200
            assert response.json['title'] == 'user2'
            target_id = response.json['id']

            when('The users have a direct')
            assert response.json['id'] == target_id

            when('The user not exists', form=Update(userId=5))
            assert status == '611 User Not Found'

            when(
                'Try to pass invalid user id in the form',
                form=Update(userId='Invalid')
            )
            assert status == '705 Invalid User Id'

            when('Try to pass empty form', form=None)
            assert status == '710 Empty Form'

            when('Blocked user tries to create a direct', form=Update(userId=1))
            assert status == '613 Not Allowed To Create Direct With This User'

        self.logout()
        self.login('blocker@example.com')

        with self.given(
            'Try to create a direct with a blocked user',
            '/apiv1/directs',
            'CREATE',
            form=dict(userId=2)
        ):
            assert status == '613 Not Allowed To Create Direct With This User'

            when('Try to pass an unauthorized request', authorization=None)
            assert status == 401

