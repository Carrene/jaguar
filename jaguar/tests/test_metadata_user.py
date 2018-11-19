from bddrest.authoring import status, response

from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestMemberMetadata(AutoDocumentationBDDTest):

    def test_metadata(self):
        with self.given('Test metadata verb', '/apiv1/members', 'METADATA'):
            assert status == 200

            fields = response.json['fields']

            assert fields['title']['maxLength'] is not None
            assert fields['title']['minLength'] is not None
            assert fields['title']['name'] is not None
            assert fields['title']['not_none'] is not None
            assert fields['title']['required'] is not None

            assert fields['phone']['maxLength'] is not None
            assert fields['phone']['minLength'] is not None
            assert fields['phone']['name'] is not None
            assert fields['phone']['not_none'] is not None
            assert fields['phone']['required'] is not None

            assert fields['email']['maxLength'] is not None
            assert fields['email']['minLength'] is not None
            assert fields['email']['name'] is not None
            assert fields['email']['not_none'] is not None
            assert fields['email']['required'] is not None

