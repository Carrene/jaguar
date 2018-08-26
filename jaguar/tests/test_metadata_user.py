from bddrest.authoring import status

from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestMetadataUser(AutoDocumentationBDDTest):

    def test_metadata(self):
        with self.given('Test metadata verb', '/apiv1/users', 'METADATA'):
            assert status == 200

