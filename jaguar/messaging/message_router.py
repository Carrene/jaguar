import aio_pika
from restfulpy.orm import DBSession

from ..models import TargetMember, Member


class MessageRouter:

    def get_members_by_target(self, target_id):
        members = DBSession.query(Member) \
            .join(TargetMember, TargetMember.member_id == Member.id) \
            .filter(TargetMember.target_id == target_id) \
            .all()
        return members

    async def route(self, envelop, member_id):
        for session, queue in session_manager.get_session(member_id):
            await channel.default_exchange.publish(
                aio_pika.Message(envelop),
                routing_key=queue
            )

