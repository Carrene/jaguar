from nanohttp import json, context, HTTPStatus, validate
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit
from sqlalchemy import or_, and_, select, func, ARRAY, Integer
from sqlalchemy.dialects.postgresql import aggregate_order_by

from ..models import Direct, User, blocked, target_member


class DirectController(ModelRestController):
    __model__ = Direct

    @authorize
    @validate(userId=dict(type_=(int, '705 Invalid User Id')))
    @json(prevent_empty_form='710 Empty Form')
    @Direct.expose
    @commit
    def create(self):
        user_id = context.form.get('userId')
        destination = DBSession.query(User) \
            .filter(User.id == user_id).one_or_none()
        if destination is None:
            raise HTTPStatus('611 User Not Found')

        current_user = DBSession.query(User) \
            .filter(User.reference_id == context.identity.reference_id) \
            .one()
        is_blocked = DBSession.query(blocked) \
            .filter(or_(
                and_(
                    blocked.c.source == user_id,
                    blocked.c.destination == current_user.id
                ),
                and_(
                    blocked.c.source == current_user.id,
                    blocked.c.destination == user_id
                )
            )) \
            .count()
        if is_blocked:
            raise HTTPStatus('613 Not Allowed To Create Direct With This User')

        source = User.current()

        cte = select([
            target_member.c.target_id.label('direct_id'),
            func.array_agg(
                aggregate_order_by(
                    target_member.c.member_id,
                    target_member.c.member_id
                )
                ,type_=ARRAY(Integer)
            ).label('members')
        ]).group_by(target_member.c.target_id).cte()

        direct = DBSession.query(Direct) \
            .join(cte, cte.c.direct_id == Direct.id) \
            .filter(cte.c.members == sorted([source.id, user_id])) \
            .one_or_none()

        if direct:
            return direct

        direct = Direct(title=destination.title, type='direct')
        direct.members = [source, destination]
        return direct

