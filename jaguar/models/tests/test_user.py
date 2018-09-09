
import pytest
from nanohttp import HTTPStatus

from jaguar.models.membership import User
from jaguar.models.target import Room


# Test target model
def test_user_model(db):
    session = db()
    user = User(
        title='example',
        username='example',
        email='example@example.com',
        access_token='access token'
    )
    session.add(user)
    session.commit()
    assert session.query(User).count() == 1
    assert user.add_to_room == True

    # Testing rooms of a user
    room = Room(title='example')
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
        title='contact',
        username='contact',
        email='contact@example.com',
        access_token='access token'
    )
    session.add(contact)
    user.contacts.append(contact)
    session.commit()
    assert len(user.contacts) == 1

    # Testing other side of relationship
    session.commit()
    user.blocked_users.append(contact)
    assert len(user.blocked_users) == 1

