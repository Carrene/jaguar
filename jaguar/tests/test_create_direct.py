from bddrest.authoring import status, given, when, Update, response

from jaguar.tests.helpers import AutoDocumentationBDDTest
from jaguar.models import User, blocked


class TestDirect(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user1 = User(
            email='user1@example.com',
            password='123456',
            title='user1'
        )
        user2 = User(
            email='user2@example.com',
            password='123456',
            title='user2',
        )
        blocker = User(
            email='blocker@example.com',
            password='123456',
            title='blocker',
        )
        blocker.blocked_users.append(user1)
        session.add_all([blocker, user2])
        session.commit()

    def test_creat_token(self):
        self.login(
            email='user1@example.com',
            password='123456',
            url='/apiv1/tokens',
            verb='CREATE',
        )

        with self.given(
            'Try to create a direct with a user',
            '/apiv1/directs',
            'CREATE',
            form=dict(userId=3)
        ):
            assert status == 200
            assert response.json['title'] == 'user2'

            when('The user not exists', form=Update(userId=5))
            assert status == '611 User Not Found'

            when(
                'Try to pass Invalid userId in the form',
                form=Update(userId='Invalid')
            )
            assert status == '705 Invalid User Id'

            when('Try to pass empty form', form=Update(userId={}))
            assert status == '710 Empty Form'

            when('Blocked user try to create a direct', form=Update(userId=1))
            assert status == '613 Not Allowed To Create Direct With This User'

        self.logout()
        self.login(
            email='blocker@example.com',
            password='123456',
            url='/apiv1/tokens',
            verb='CREATE',
        )

        with self.given(
            'Try to create direct with blocked user',
            '/apiv1/directs/',
            'CREATE',
            form=dict(userId=2)
        ):
            assert status == '613 Not Allowed To Create Direct With This User'

            when('Try to pass an unauthorized request', authorization=None)
            assert status == 401

