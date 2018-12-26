from restfulpy.orm import DBSession

from jaguar.messaging.queues import queue_manager
from jaguar.messaging.sessions import session_manager
from jaguar.models import TargetMember, Member


class MessageRouter:

    def get_members_by_target(self, target_id):
        import pudb; pudb.set_trace()  # XXX BREAKPOINT
        members = DBSession.query(Member).get(1)
#            .join(TargetMember, TargetMember.member_id == Member.id) \
#            .filter(TargetMember.target_id == target_id) \
#            .all()
        return members

    async def route(self, envelop):
        members = self.get_members_by_target(envelop['target_id'])
        for member in members:
            active_sessions = await session_manager.get_sessions(member.id)
            for session, queue in active_sessions:
                await queue_manager.enqueue_async(queue, envelop)


message_router = MessageRouter()

