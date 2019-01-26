from sqlalchemy.orm import aliased
from nanohttp import json, context, settings, HTTPNotFound
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from ..messaging import queues
from ..models import Mention, Member, Direct, TargetMember, Target
from ..validators import mention_validator


class MentionController(ModelRestController):
    __model__ = Mention

    def __init__(self, target=None, member=None):
        self.target = target
        self.member = member

    @authorize
    @mention_validator
    @json
    @commit
    def mention(self):
        mention = Mention()
        mention.body = context.form.get('body')

        if not (self.target or self.member):
            raise HTTPNotFound()

        if self.target:
            mention.target_id = self.target.id
            mention.sender_id = Member.current().id
        else:
            mentioner = Member.current()
            mentioned = self.member

            t = aliased(Target)
            tm1 = aliased(TargetMember)
            tm2 = aliased(TargetMember)

            target_member = DBSession.query(tm1) \
                .join(tm2, tm1.target_id == tm2.target_id) \
                .filter(tm1.member_id == mentioned.id) \
                .filter(tm2.member_id == mentioner.id) \
                .join(t, t.id == tm1.target_id) \
                .filter(t.type == 'direct') \
                .one_or_none()

            mention.sender_id = mentioner.id
            if target_member is None:
                direct = Direct(members=[mentioner, mentioned])
                DBSession.add(direct)
                DBSession.flush()
                mention.target_id = direct.id
            else:
                mention.target_id = target_member.target_id

        DBSession.add(mention)
        queues.push(settings.messaging.workers_queue, mention.to_dict())

        return mention

