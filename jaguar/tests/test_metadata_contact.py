from bddrest.authoring import status

from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestContactMetadata(AutoDocumentationBDDTest):

    def test_metadata(self):
        with self.given('Test metadata verb', '/apiv1/contacts', 'METADATA'):
            assert status == 200

