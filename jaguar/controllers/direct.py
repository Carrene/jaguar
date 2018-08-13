from sqlalchemy import or_, and_
from nanohttp import json, context, HTTPStatus, validate
from restfulpy.controllers import ModelRestController
from restfulpy.authorization import authorize
from restfulpy.orm import DBSession, commit

from ..models import Direct, User, blocked


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
            raise HTTPStatus('613 Not Allowed To Create Direct With This User')

        source = User.current()
        direct = Direct(title=destination.title, type='direct')
        direct.members = [source, destination]
        return direct

