from restfulpy.orm import DBSession
from jaguar.models import Member, Room


def insert(): # pragma: no cover

    user1 = Member(
        email='user1@example.com',
        title='user1',
        access_token='access token1',
        reference_id=2
    )
    user2 = Member(
        email='user2@example.com',
        title='user2',
        access_token='access token2',
        reference_id=3
    )
    DBSession.add(user2)
    room = Room(
        title='example',
        members=[user1]
    )
    DBSession.add(room)
    DBSession.commit()

