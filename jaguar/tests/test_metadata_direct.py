from bddrest.authoring import status

from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestMetadataDirect(AutoDocumentationBDDTest):

    def test_metadada(self):
        with self.given('Test metadata verb', '/apiv1/directs', 'METADATA'):
            assert status == 200

