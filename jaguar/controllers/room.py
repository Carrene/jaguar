from sqlalchemy import and_, or_
from nanohttp import json, context, validate, HTTPStatus
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from ..models import Target, Room, blocked, User, target_member


class RoomController(ModelRestController):
    __model__ = Target

    @authorize
    @json
    @Room.expose
    @commit
    @validate(
        title=dict(
            min_length=(4, '701 Must Be Greater Than 4 Charecters'),
            max_length=(32, '702 Must Be Less Than 32 Charecters'),
            required='703 Room Title Is Required',
        )
    )
    def create(self):
        title = context.form.get('title')
        is_exist = DBSession.query(Room) \
            .filter(
                Room.title == title, Room.owner_id == context.identity.id
            ) \
            .count()
        if  is_exist:
            raise HTTPStatus('615 Room Already Exists')

        room = Room(title=title)
        member = User.current()
        room.administrators.append(member)
        room.members.append(member)

        room.owner = member
        DBSession.add(room)
        return room

    @json
    @Room.expose
    @commit
    def add(self, id: int):
        user_id = context.form.get('userId')
        room = DBSession.query(Room).filter(Room.id == id).one_or_none()
        if room is None:
            raise HTTPStatus('612 Room Not Found')

        is_member = DBSession.query(target_member) \
            .filter(
                target_member.c.target_id == id,
                target_member.c.member_id == user_id
            ) \
            .count()
        if is_member:
            raise HTTPStatus('604 Already Added To Target')

        user = DBSession.query(User).filter(User.id == user_id).one_or_none()
        if user is None:
            raise HTTPStatus('611 User Not Found')

        if not user.add_to_room:
            raise HTTPStatus('602 Not Allowed To Add This Person To Any Room')

        is_blocked = DBSession.query(blocked) \
            .filter(or_(
                and_(
                    blocked.c.source == user_id,
                    blocked.c.destination == context.identity.id
                ),
                and_(
                    blocked.c.source == context.identity.id,
                    blocked.c.destination == user_id
                )
            )) \
            .count()
        if is_blocked:
            raise HTTPStatus('601 Not Allowed To Add User To Any Room')

        room.members.append(user)
        return room

