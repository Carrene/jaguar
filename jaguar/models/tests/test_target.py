from jaguar.models.target import Room
from jaguar.models.user import User

def test_target_model(db):
    session = db()
    room = Room(title='example', type='room')
    session.add(room)
    session.commit()
    assert session.query(Room).count() == 1

    # Test members of a room
    member = User(
        title='example',
        user_name='example',
        email='example@example.com'
    )
    session.add(member)
    room.members.append(member)
    session.commit()

    # Since the selectin loading is used to load relations,
    # the relation is already load.
    assert room.members[0].title == 'example'

    # Test administrators of a room
    administrator = User(
        title='administrator',
        user_name='administrator',
        email='administrator@example.com'
    )
    session.add(administrator)
    session.commit()
    room.administrators.append(administrator)
    session.commit()
    assert room.administrators[0].title == 'administrator'
