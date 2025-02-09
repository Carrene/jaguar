from bddrest.authoring import when, Update, Remove, status, response
from restfulpy.principal import JWTPrincipal

from jaguar.models.membership import Member
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestAddToContact(AutoDocumentationBDDTest):

    def test_create_user(self):
        token = JWTPrincipal(dict(
            email='user1@example.com',
            title='user1',
            firstName='user1_first_name',
            lastName='user1_last_name',
            referenceId=2
        )).dump().decode()

        with cas_mockup_server(), self.given(
            'Create a member',
            '/apiv1/members',
            'ENSURE',
            headers=dict(
                authorization=token,
                x_oauth2_access_token='access token1'
            ),
            form=dict(title='example')
        ):
            assert status == 200
            assert response.json['title'] == 'user1'

            when(
                'Access token is not in headers',
                headers=Remove('x_oauth2_access_token')
            )
            assert status == 400

