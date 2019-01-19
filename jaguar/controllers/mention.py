from nanohttp import json, context
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController

from ..models import Mention
from ..validators import mention_validator


class MentionController(ModelRestController):
    __model__ = Mention

    @authorize
    @mention_validator
    @json
    @Mention.expose
    def mention(self):
        mention = Mention()
        mention.reference = context.form.get('reference')
        return mention

