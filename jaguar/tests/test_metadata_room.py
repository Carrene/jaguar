from bddrest.authoring import status

from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestMetadataRoom(AutoDocumentationBDDTest):

    def test_metadata(self):
        with self.given('Test metadata verb', '/apiv1/rooms', 'METADATA'):
            assert status == 200

