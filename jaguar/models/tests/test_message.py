
from jaguar.models.envelop import Message
from jaguar.models.membership import User
from jaguar.models.target import Room


def test_message_model(db):
    session = db()
    member = User(
        title='example',
        username='example',
        email='example@example.com',
        access_token='access token',
    )
    session.add(member)
    session.flush()
    room = Room(title='example', type='room')
    session.add(room)
    session.flush()

    # Test message model. As every message should have a sender
    # to be send, sender_id and target_id can not be nullable
    message = Message(
        mime_type='message',
        body='Hello world!',
        sender_id=member.id,
        target_id=room.id,
    )

    session.add(message)
    session.flush()
    assert session.query(Message).count() == 1

    # Test target id of a message
    assert message.target_id == 1

    # Test messages of a room
    assert len(room.messages) == 1
    assert room.messages[0].body == 'Hello world!'

    # Test messages of a user
    message.seen_by.append(member)
    session.commit()
    assert len(message.seen_by) == 1

