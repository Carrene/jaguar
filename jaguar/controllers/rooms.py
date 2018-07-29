
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession
from nanohttp import json, context, validate

from jaguar.models import Target, Room


class RoomsController(ModelRestController):
    __model__ = Target

    @validate(
        title=dict(
            min_length=(4, '701 Must Be Greater Than Minimum Length'),
            max_length=(32, '702 Exceed Max Length'),
            required=(True, '703 Room Title Is Required'),
        )
    )
    @json
    def create(self):
        title = context.form.get('title')
        room = Room(title=title)
        DBSession.add(room)

        return room
