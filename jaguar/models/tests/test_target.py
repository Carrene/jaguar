
from jaguar.models.target import Room
from jaguar.models.membership import User


def test_target_model(db):
    session = db()
    room = Room(title='example', type='room')
    session.add(room)
    session.commit()
    assert session.query(Room).count() == 1

    # Test members of a room
    member = User(
        title='example',
        password='123456',
        user_name='example',
        email='example@example.com'
    )
    session.add(member)
    room.members.append(member)
    room.owner = member
    session.commit()
    # Since the selectin loading is used to load relations,
    # the relation is already load.
    assert room.members[0].title == 'example'

    # Test administrators of a room
    administrator = User(
        title='administrator',
        password='123456',
        user_name='administrator',
        email='administrator@example.com'
    )
    session.add(administrator)
    session.commit()
    room.administrators.append(administrator)
    session.commit()
    assert room.administrators[0].title == 'administrator'
    assert room.owner_id == 1
