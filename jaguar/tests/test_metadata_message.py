from bddrest.authoring import status, response

from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestMessageMetadata(AutoDocumentationBDDTest):

    def test_metadata(self):
        with self.given('Test metadata verb', '/apiv1/messages', 'METADATA'):
            assert status == 200
            assert 'isMine' in response.json['fields']
            assert 'attachment' in response.json['fields']

