
from nanohttp import json, context, HTTPUnauthorized, HTTPStatus
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession

from ..models import Target, target_member
from .message import MessageController


class TargetController(ModelRestController):
    __model__ = Target

    def __call__(self, *remaining_paths):
        if len(remaining_paths) > 1 and remaining_paths[1] == 'messages':
            target = self.get_target(remaining_paths[0])
            return MessageController(target)(*remaining_paths[2:])

        return super().__call__(*remaining_paths)

    def get_target(self, id):
        try:
            int(id)
        except:
            raise HTTPStatus('706 Invalid Target Id')
        target = DBSession.query(Target).filter(Target.id == id).one_or_none()
        if target is None:
            raise HTTPStatus('614 Target Not Exist')

        return target

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

