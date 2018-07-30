from nanohttp import json, context, validate
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession

from jaguar.models import Target, Room
from jaguar.models import User


class RoomController(ModelRestController):
    __model__ = Target

    @authorize
    @json
    @validate(
        title=dict(
            min_length=(4, '701 Must Be Greater Than 4 Charecters'),
            max_length=(32, '702 Must Be Less Than 32 Charecters'),
            required=(True, '703 Room Title Is Required'),
        )
    )
    def create(self):
        title = context.form.get('title')

        room = Room(title=title)
        member = User.current()
        room.administrators.append(member)
        room.members.append(member)
        room.owner = member

        DBSession.add(room)
        DBSession.commit()

        return room.to_dict()

