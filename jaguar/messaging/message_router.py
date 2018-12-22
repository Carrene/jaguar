import aio_pika
from nanohttp import settings
from restfulpy.orm import DBSession

from ..models import TargetMember, Member
from .websocket import session_manager, queue_manager


class MessageRouter:

    def get_members_by_target(self, target_id):
        members = DBSession.query(Member) \
            .join(TargetMember, TargetMember.member_id == Member.id) \
            .filter(TargetMember.target_id == target_id) \
            .all()
        return members

    async def route(self, envelop):
        members = self.get_members_by_target(envelop['target_id'])
        for member in members:
            active_sessions = await session_manager.get_sessions(member.id)
            for session, queue in active_sessions:
                await queue_manager.enqueue_async(queue, envelop)

