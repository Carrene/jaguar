from bddrest.authoring import status

from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestDirectMetadata(AutoDocumentationBDDTest):

    def test_metadada(self):
        with self.given('Test metadata verb', '/apiv1/directs', 'METADATA'):
            assert status == 200

