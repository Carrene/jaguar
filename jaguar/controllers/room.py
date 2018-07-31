from nanohttp import json, context, validate, HTTPStatus
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from jaguar.models import Target, Room, blocked_user
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

    @json
    @Room.expose
    @commit
    def add(self, room_id : int):
        user_id = context.form.get('user_id')
        room = DBSession.query(Room).filter_by(id=room_id).one()
        if int(user_id) in room.to_dict()['member_ids']:
            raise HTTPStatus('604 Already Added To Target')
        user = DBSession.query(User).filter_by(id = user_id).one()
        if not user.add_to_room:
            raise HTTPStatus('602 Not Allowed To Add This Person To Any Room')
        room.members.append(user)
        return room
