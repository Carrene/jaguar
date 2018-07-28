
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession
from nanohttp import json, context, validate

from jaguar.models import Target, Room


class RoomsController(ModelRestController):
    __model__ = Target

    @validate(
        title=dict(
            min_length=(4, '701 Must be greater than minimum length'),
            max_length=(32, '702 Exceed max length'),
            required=(True, '703 Room title is required'),
        )
    )
    @json
    def create(self):
        title = context.form.get('title')
        room = Room(title=title)
        DBSession.add(room)

        return room
