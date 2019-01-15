from restfulpy.orm import DBSession

from .models import Member, Room, Direct


def insert():
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
    room = Room(
        title='example',
        members=[user1]
    )
    direct = Direct(members=[user1, user2])

    DBSession.add(room)
    DBSession.add(direct)
    DBSession.commit()

