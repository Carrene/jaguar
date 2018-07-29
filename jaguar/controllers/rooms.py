
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession
from nanohttp import json, context, validate

from jaguar.models import Target, Room


class RoomController(ModelRestController):
    __model__ = Target

    @validate(
        title=dict(
            min_length=(4, '701 Must Be Greater Than 4 Charecters'),
            max_length=(32, '702 Must Be Less Than 32 Charecters'),
            required=(True, '703 Room Title Is Required'),
        )
    )
    @json
    def create(self):
        title = context.form.get('title')
        room = Room(title=title)
        DBSession.add(room)

        return room
