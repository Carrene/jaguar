from bddrest.authoring import status, response

from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestMessageMetadata(AutoDocumentationBDDTest):

    def test_metadata(self):
        with self.given('Test metadata verb', '/apiv1/messages', 'METADATA'):
            assert status == 200
            assert 'isMine' in response.json['fields']
            assert 'attachment' in response.json['fields']

            fields = response.json['fields']

            assert fields['body']['minLength'] is not None
            assert fields['body']['name'] is not None
            assert fields['body']['not_none'] is not None
            assert fields['body']['required'] is not None
            assert fields['body']['protected'] is not None

            assert fields['mimetype']['maxLength'] is not None
            assert fields['mimetype']['name'] is not None
            assert fields['mimetype']['not_none'] is not None
            assert fields['mimetype']['required'] is not None
            assert fields['mimetype']['protected'] is not None

