

from nanohttp import json, context, HTTPUnauthorized, HTTPStatus
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession

from ..models import Target, Room, target_member
from .message import MessageController


class SubscribeTargetController(ModelRestController):
    __model__ = Target

    @authorize
    @json
    @Target.expose
    def list(self):
        query = DBSession.query(Target) \
            .join(target_member) \
            .filter(
                Target.id == target_member.c.target_id,
                target_member.c.member_id == context.identity.id
            )
        return query

