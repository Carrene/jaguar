from nanohttp import json, context
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from ..models import Mention, Member
from ..validators import mention_validator


class MentionController(ModelRestController):
    __model__ = Mention

    @authorize
    @mention_validator
    @json
    @Mention.expose
    @commit
    def mention(self, target_id):

        mention = Mention()
        mention.body = context.form.get('body')
        mention.target_id = int(target_id)
        mention.sender_id = Member.current().id
        DBSession.add(mention)

        return mention

