from bddrest.authoring import status, response

from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestRoomMetadata(AutoDocumentationBDDTest):

    def test_metadata(self):
        with self.given('Test metadata verb', '/apiv1/rooms', 'METADATA'):
            assert status == 200
            fields = response.json['fields']

            assert fields['type']['maxLength'] is not None
            assert fields['type']['minLength'] is not None
            assert fields['type']['name'] is not None
            assert fields['type']['not_none'] is not None
            assert fields['type']['required'] is not None

