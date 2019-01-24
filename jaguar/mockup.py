from sqlalchemy import and_
from sqlalchemy.orm import aliased
from restfulpy.orm import DBSession

from .models import Member, Room, Direct, TargetMember, Target


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
        members=[god, user1, user2, user3]
    )
    direct1 = Direct(members=[god, user1])
    direct2 = Direct(members=[god, user2])

    DBSession.add(room)
    DBSession.add(direct1)
    DBSession.add(direct2)
    DBSession.commit()

    tm1 = aliased(TargetMember)
    tm2 = aliased(TargetMember)
    t = aliased(Target)
    target = DBSession.query(tm1) \
        .join(tm2, tm1.target_id == tm2.target_id) \
        .filter(tm1.member_id == 1) \
        .filter(tm2.member_id == 2) \
        .join(t, t.id == tm1.target_id) \
        .filter(t.type == 'direct') \
        .all()

    for i in target:
        print(i.target_id)



# select t.id from target_member tm1 join target_member tm2 on tm1.target_id
# = tm2.target_id AND tm1.member_id != tm2.member_id AND tm1.member_id = 1 AND tm2.member_id = 2 join target t on t.id = tm1.target_id and t.type = 'direct';


