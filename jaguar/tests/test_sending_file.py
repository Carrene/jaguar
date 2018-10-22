
from os.path import join, dirname, abspath, exists
import shutil
import functools

from sqlalchemy_media import StoreManager, FileSystemStore
from sqlalchemy_media.exceptions import ContentTypeValidationError
from bddrest.authoring import given, when, Update, status, response, Remove

from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server
from jaguar.models import User, Room, Direct


this_dir = abspath(join(dirname(__file__)))
text_path = join(this_dir, 'stuff', 'text_file.txt')
tex_path = join(this_dir, 'stuff', 'sample_tex_file.tex')
image_path = join(this_dir, 'stuff', '150x150.png')


class TestFileSharing(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user1 = User(
            email='user1@example.com',
            title='user1',
            access_token='access token1',
            reference_id=2
        )
        room = Room(title='example', type='room')
        direct = Direct(title='direct', type='direct')
        session.add(user1)
        session.add(room)
        session.commit()

    def test_attach_file_to_message(self):
        self.login('user1@example.com')

        with cas_mockup_server(), self.given(
            'Send a message to a target',
            '/apiv1/targets/id:1/messages',
            'SEND',
            multipart=dict(
                body='hello world!',
                mimetype='image/png',
                attachment=image_path
            )
        ):
            assert status == 200
            assert response.json['body'] == 'hello world!'
            assert response.json['isMine'] == True
            assert 'Attachment' in response.json
            assert response.json['Attachment']['content_type'] == 'image/png'

            when(
                'does not match file content type',
                multipart = Update(attachment=tex_path)
            )
            assert status == '710 The Mimetype Does Not Match The File Type'

            when(
                'mime type does not match content type',
                multipart=Update(attachment=text_path)
            )
            assert status == '710 The Mimetype Does Not Match The File Type'

