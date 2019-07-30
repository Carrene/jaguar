from restfulpy.orm import DBSession
from sqlalchemy.orm import aliased

from .models import Member, Room, Direct, TargetMember, Target


def insert():
    god = Member(
        id=1,
        email='god@example.com',
        title='GOD',
        first_name='First name',
        last_name='Last name',
        access_token='access token',
        reference_id=1
    )
    user1 = Member(
        id=2,
        email='user1@example.com',
        title='user_1',
        first_name='user1_first_name',
        last_name='user1_last_name',
        access_token='access token1',
        reference_id=2
    )
    user2 = Member(
        id=3,
        email='user2@example.com',
        title='user_2',
        first_name='user2_first_name',
        last_name='user2_last_name',
        access_token='access token2',
        reference_id=3
    )
    user3 = Member(
        id=4,
        email='user3@example.com',
        title='user_3',
        first_name='user3_first_name',
        last_name='user3_last_name',
        access_token='access token3',
        reference_id=4
    )
    room = Room(
        title='example',
        members=[god, user1, user2, user3]
    )
    direct1 = Direct(members=[god, user1])
    direct2 = Direct(members=[god, user2])

    DBSession.add(room)
    DBSession.add(direct1)
    DBSession.add(direct2)
    DBSession.commit()

