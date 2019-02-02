import io
from os.path import join, dirname, abspath, exists
import shutil
import functools

from sqlalchemy_media import StoreManager, FileSystemStore
from sqlalchemy_media.exceptions import ContentTypeValidationError
from bddrest.authoring import given, when, Update, status, response, Remove

from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server
from jaguar.models import Member, Room, Direct


THIS_DIR = abspath(join(dirname(__file__)))
TEXT_PATH = join(THIS_DIR, 'stuff', 'text_file.txt')
TEX_PATH = join(THIS_DIR, 'stuff', 'sample_tex_file.tex')
IMAGE_PATH = join(THIS_DIR, 'stuff', '150x150.png')
MAXIMUM_IMAGE_PATH = join(THIS_DIR, 'stuff', 'maximum-length.jpg')
PDF_PATH = join(THIS_DIR, 'stuff', 'sample.pdf')
DOC_PATH = join(THIS_DIR, 'stuff', 'sample.doc')
DOCX_PATH = join(THIS_DIR, 'stuff', 'sample.docx')


class TestFileSharing(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user1 = Member(
            email='user1@example.com',
            title='user1',
            access_token='access token1',
            reference_id=2
        )
        room = Room(
            title='example',
            type='room',
            members=[user1],
        )
        direct = Direct()
        session.add(user1)
        session.add(room)
        session.commit()

    def test_attach_file_to_message(self):
        self.login('user1@example.com')

        with cas_mockup_server(), open(IMAGE_PATH, 'rb') as f ,self.given(
            'Send a message to a target',
            '/apiv1/targets/id:1/messages',
            'SEND',
            multipart=dict(
                body='hello world!',
                mimetype='image/png',
                attachment=io.BytesIO(f.read())
            )
        ):
            assert status == 200
            assert response.json['body'] == 'hello world!'
            assert response.json['isMine'] is True
            assert 'attachment' in response.json


            with open(PDF_PATH, 'rb') as f:
                when(
                    'File format is .pdf',
                    multipart=Update(
                        attachment=io.BytesIO(f.read()),
                        mimetype='application/pdf'
                    )
                )
                assert status == 200
                assert response.json['mimetype'] == 'application/pdf'


            with open(DOC_PATH, 'rb') as f:
                when(
                    'File format is .doc',
                    multipart=Update(
                        attachment=io.BytesIO(f.read()),
                        mimetype='application/CDFV2'
                    )
                )
                assert status == 200
                assert response.json['mimetype'] == 'application/CDFV2'

            with open(DOCX_PATH, 'rb') as f:
                when(
                    'File format is .doc',
                    multipart=Update(
                        attachment=io.BytesIO(f.read()),
                        mimetype='application/zip'
                    )
                )
                assert status == 200
                assert response.json['mimetype'] == 'application/zip'


            with open(TEX_PATH, 'rb') as f:
                when(
                    'does not match file content type',
                    multipart=Update(attachment=io.BytesIO(f.read()))
                )
                assert status == '710 The Mimetype Does Not Match The File Type'

            with open(TEXT_PATH, 'rb') as f:
                when(
                    'mime type does not match content type',
                    multipart=Update(attachment=io.BytesIO(f.read()))
                )
                assert status == '710 The Mimetype Does Not Match The File Type'

            with open(MAXIMUM_IMAGE_PATH, 'rb') as f:
                when(
                    'Image size is more than maximum length',
                    multipart=Update(
                        mimetype='image/jpeg',
                        attachment=io.BytesIO(f.read()))
                )
                assert status == 413

