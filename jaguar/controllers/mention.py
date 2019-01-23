from nanohttp import json, context, settings
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from ..messaging import queues
from ..models import Mention, Member, Direct
from ..validators import mention_validator


class MentionController(ModelRestController):
    __model__ = Mention

    def __init__(self, target=None, member=None):
        self.target = target
        self.member = member

    @authorize
    @mention_validator
    @json
    @Mention.expose
    @commit
    def mention(self, target_id):
        mention = Mention()
        mention.body = context.form.get('body')
        if self.target:
            mention.target_id = int(target_id)
        else:
            direct = DBSession.query(

        mention.sender_id = Member.current().id
        DBSession.add(mention)

        queues.push(settings.messaging.workers_queue, mention.to_dict())

        return mention

