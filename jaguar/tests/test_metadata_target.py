from bddrest.authoring import status

from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestTargetMetadata(AutoDocumentationBDDTest):

    def test_metadata(self):
        with self.given('Test metadata verb', '/apiv1/targets', 'METADATA'):
            assert status == 200

