from sqlalchemy import and_, or_
from nanohttp import json, context, validate, HTTPStatus, HTTPNotFound
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from ..models import Target, Room, member_block, Member, TargetMember


class RoomController(ModelRestController):
    __model__ = Target

    @authorize
    @json
    @Room.expose
    @commit
    @validate(
        title=dict(
            min_length=(4, '701 Must Be Greater Than 4 Charecters'),
            max_length=(50, '702 Must Be Less Than 50 Charecters'),
            required='703 Room Title Is Required',
        )
    )
    def create(self):
        title = context.form.get('title')
        current_user = DBSession.query(Member) \
            .filter(Member.reference_id == context.identity.reference_id) \
            .one()
        is_exist = DBSession.query(Room) \
            .filter(
                Room.title == title, Room.owner_id == current_user.id
            ) \
            .count()
        if  is_exist:
            raise HTTPStatus('615 Room Already Exists')

        room = Room(title=title)
        member = Member.current()
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
        requested_user = DBSession.query(Member) \
            .filter(Member.reference_id == user_id) \
            .one_or_none()
        if requested_user is None:
            raise HTTPStatus('611 Member Not Found')

        room = DBSession.query(Room).filter(Room.id == id).one_or_none()
        if room is None:
            raise HTTPStatus('612 Room Not Found')

        is_member = DBSession.query(TargetMember) \
            .filter(
                TargetMember.target_id == id,
                TargetMember.member_id == requested_user.id
            ) \
            .count()
        if is_member:
            raise HTTPStatus('604 Already Added To Target')


        if not requested_user.add_to_room:
            raise HTTPStatus('602 Not Allowed To Add This Person To Any Room')

        current_user = DBSession.query(Member) \
            .filter(Member.reference_id == context.identity.reference_id) \
            .one()
        is_blocked = DBSession.query(member_block) \
            .filter(or_(
                and_(
                    member_block.c.member_id == requested_user.id,
                    member_block.c.bocked_member_id == current_user.id
                ),
                and_(
                    member_block.c.member_id == current_user.id,
                    member_block.c.bocked_member_id == requested_user.id
                )
            )) \
            .count()
        if is_blocked:
            raise HTTPStatus('601 Not Allowed To Add Member To Any Room')

        room.members.append(requested_user)
        return room

    @authorize
    @json
    @Target.expose
    def list(self):
        current_user = DBSession.query(Member) \
            .filter(Member.reference_id == context.identity.reference_id) \
            .one()
        query = DBSession.query(Room)
        if not context.identity.is_in_roles('admin'):
            query =  query.filter(
                Room.owner_id == current_user.id
            )

        return query

    @authorize
    @validate(
        memberId=dict(
            type_=(int, '705 Invalid Member Id'),
            required='709 Member Id Is Required',
        )
    )
    @json
    @Room.expose
    @commit
    def kick(self, id):
        try:
            id = int(id)
        except(ValueError, TypeError):
            raise HTTPNotFound()

        room = DBSession.query(Room).filter(Room.id == id).one_or_none()
        if room is None:
            raise HTTPNotFound()

        member_id = context.form.get('memberId')
        user = DBSession.query(Member).filter(Member.id == member_id).one_or_none()
        if user is None:
            raise HTTPStatus('611 Member Not Found')

        is_member = DBSession.query(Member) \
            .filter(
                TargetMember.target_id == id,
                TargetMember.member_id == member_id
            ) \
            .count()
        if not is_member:
            raise HTTPStatus('617 Not A Member')

        DBSession.query(TargetMember) \
            .filter(
                TargetMember.target_id == id,
                TargetMember.member_id == member_id
            ) \
            .delete()
        return room

