from jaguar.models.user import User
from jaguar.models.target import Room

# Test target model
def test_user_model(db):
    session = db()
    user = User(
        title = 'example',
        user_name = 'example',
        email = 'example@example.com'
    )
    session.add(user)
    session.commit()
    assert session.query(User).count() == 1

    # Testing rooms of a user
    room = Room(title = 'example')
    session.add(room)
    user.rooms.append(room)
    session.commit()

    # Since the selectin loading is used to load relations,
    # the relation is already load.
    assert user.rooms[0].title == 'example'

    # Testing rooms of an administrator
    user.administrator_of.append(room)
    session.commit()

    assert user.administrator_of[0].title == 'example'
    assert user.administrator_of[0].id == 1

    # Testing relationship between User and User ( As contactlist)
    contact = User(
        title = 'contact',
        user_name = 'contact',
        email = 'contact@example.com'
    )
    session.add(contact)
    user.contact.append(contact)
    session.commit()
    assert len(user.contact) == 1

    # Testing other side of relationship
    contact.contact_parent = user
    session.commit()
    assert contact.contact_parent.title == 'example'
