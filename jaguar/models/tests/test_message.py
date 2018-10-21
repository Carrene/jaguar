from os.path import join, dirname, abspath, exists
import shutil
import functools

from sqlalchemy_media import StoreManager, FileSystemStore
from sqlalchemy_media.exceptions import ContentTypeValidationError
import pytest

from jaguar.models.envelop import Message, FileAttachment
from jaguar.models.membership import User
from jaguar.models.target import Room


this_dir = abspath(join(dirname(__file__)))
text_path = join(this_dir, 'stuff', 'text_file.txt')
pdf_path = join(this_dir, 'stuff', 'test.pdf')
image_path = join(this_dir, 'stuff', '150x150.png')
temp_path = join(this_dir, 'temp')
base_url = 'http://static1.example.orm'


StoreManager.register(
    'fs',
    functools.partial(FileSystemStore, temp_path, base_url),
    default=True
)


def test_message_model(db):
    session = db()
    if exists(temp_path):
        shutil.rmtree(temp_path)

    with StoreManager(session):
        message1 = Message(
            mimetype='message1',
            body='This is message 1',
            attachment=text_path
        )
        message2 = Message(
            mimetype='message2',
            body='This is message 2',
        )
        message3 = Message(
            mimetype='message3',
            body='This is message 3',
        )
        user = User(
            title='user',
            username='user',
            email='user@example.com',
            access_token='access token',
            reference_id=1,
            messages=[message1, message2, message3]
        )
        room = Room(
            title='example',
            type='room',
            messages=[message1, message2, message3],
            members=[user]
        )
        session.add(room)
        session.commit()

        # Test message model. As every message should have a sender
        # to be send, sender_id and target_id can not be nullable
        assert session.query(Message).count() == 3

        # Test target id of a message
        assert message1.target_id == 1

        # Test messages of a room
        assert len(room.messages) == 3
        assert room.messages[0].body == 'This is message 1'

        # Test messages of a user
        message1.seen_by.append(user)
        session.commit()
        assert len(message1.seen_by) == 1

        # The replied_to is a many to one relationship
        message2.reply_to = message1
        message3.reply_to = message1
        session.commit()
        assert message2.reply_root == message1.id
        assert message3.reply_root == message1.id
        with pytest.raises(ContentTypeValidationError):
                 message2.attachment = pdf_path
