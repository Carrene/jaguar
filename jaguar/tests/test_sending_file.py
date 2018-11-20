import io
from os.path import join, dirname, abspath, exists
import shutil
import functools

from sqlalchemy_media import StoreManager, FileSystemStore
from sqlalchemy_media.exceptions import ContentTypeValidationError
from bddrest.authoring import given, when, Update, status, response, Remove

from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server
from jaguar.models import Member, Room, Direct


this_dir = abspath(join(dirname(__file__)))
text_path = join(this_dir, 'stuff', 'text_file.txt')
tex_path = join(this_dir, 'stuff', 'sample_tex_file.tex')
image_path = join(this_dir, 'stuff', '150x150.png')
maximum_image_path = join(this_dir, 'stuff', 'maximum-length.jpg')


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

        with cas_mockup_server(), open(image_path, 'rb') as f ,self.given(
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

            when(
                'Image size is more than maximum length',
                multipart=Update(
                    mimetype='image/jpeg',
                    attachment=maximum_image_path)
            )
            assert status == 413

