
from nanohttp import json, context, HTTPUnauthorized, HTTPStatus, HTTPNotFound
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession

from ..models import Target, Room
from .message import MessageController
from .mention import MentionController


class TargetController(ModelRestController):
    __model__ = Target

    def __call__(self, *remaining_paths):
        if len(remaining_paths) > 1 and remaining_paths[1] == 'messages':
            return MessageController()(remaining_paths[0], *remaining_paths[2:])

        if len(remaining_paths) > 1 and remaining_paths[1] == 'mentions':
            target = self.get_target(remaining_paths[0])
            return MentionController()(remaining_paths[0], *remaining_paths[2:])

        return super().__call__(*remaining_paths)

    def get_target(self, id):
        try:
            int(id)
        except:
            raise HTTPStatus('706 Invalid Target Id')
        target = DBSession.query(Target).filter(Target.id == id).one_or_none()
        if target is None:
            raise HTTPNotFound('Target Not Exists')

        return target

