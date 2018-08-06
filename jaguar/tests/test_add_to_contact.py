
from restfulpy.orm import DBSession
from nanohttp import context
from bddrest.authoring import response, when, Update, Remove, status

from jaguar.models.membership import User
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestAddToContact(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user = User(
            email='user@example.com',
            title='user',
            password='123456',
        )
        user.is_active = True
        user2 = User(
            email='user2@example.com',
            title='user2',
            password='123456',
        )
        contact1 = User(
            email='contact1@example.com',
            title='contact1',
            password='123456',
        )
        contact2 = User(
            email='contact2@example.com',
            title='contact2',
            password='123456',
        )
        user.contacts.append(contact2)
        contact1.contacts.append(user2)
        session.add_all([user,contact1])
        session.commit()

    def test_add_user_to_contact(self):
        self.login(
            email='user@example.com',
            password='123456',
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'Add a user to contacts',
            '/apiv1/contacts',
            verb='ADD',
           form=dict(userId=3),
        ):
            assert status == 200
            user = DBSession.query(User).filter(User.id == 1).one()
            assert len(user.contacts) == 2

            when('The user id already added to contact',form=Update(userId=2))
            assert status == '603 Already Added To Contacts'

            when('Try to add not existing user', form=Update(userId=6))
            assert status == '611 User Not Found'

            when(
                'Try to request with invalid user id',
                form=Update(userId='invalid')
            )
            assert status == '705 Invalid User Id'

            when('Request without issuing userId', form=Remove('userId'))
            assert status == '709 User Id Is Required'

            when('Unauthorization request', authorization=None)
            assert status == 401

