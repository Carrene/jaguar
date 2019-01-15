from restfulpy.orm import DBSession

from jaguar.messaging import queues, sessions
from jaguar.models import TargetMember, Member


def get_members_by_target(target_id):
    # FIXME: Use async sqlalchemy
    members = DBSession.query(Member) \
        .join(TargetMember, TargetMember.member_id == Member.id) \
        .filter(TargetMember.target_id == target_id) \
        .all()
    return members


async def route(envelop):
    members = get_members_by_target(envelop['targetId'])
    for member in members:
        async for session, queue in sessions.get_sessions(member.id):
            envelop['isMine'] = member.id == envelop['senderId']
            envelop['sessionId'] = session.decode()
            await queues.push_async(queue, envelop)

