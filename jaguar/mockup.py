from restfulpy.orm import DBSession

from .models import Member, Room, Direct


def insert():
    god = Member(
        id=1,
        email='god@example.com',
        title='GOD',
        access_token='access token',
        reference_id=1
    )
    user1 = Member(
        id=2,
        email='user1@example.com',
        title='user_1',
        access_token='access token1',
        reference_id=2
    )
    user2 = Member(
        id=3,
        email='user2@example.com',
        title='user_2',
        access_token='access token2',
        reference_id=3
    )
    user3 = Member(
        id=4,
        email='user3@example.com',
        title='user_3',
        access_token='access token3',
        reference_id=4
    )
    room = Room(
        title='example',
        members=[user1]
    )
    direct = Direct(members=[god, user1, user2, user3])

    DBSession.add(room)
    DBSession.add(direct)
    DBSession.commit()

