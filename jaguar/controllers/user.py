
from sqlalchemy import or_
from nanohttp import json, context, HTTPStatus, settings, validate, \
    HTTPNotFound
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession
from restfulpy.authorization import authorize

from ..models import User


class UserController(ModelRestController):
    __model__ = User

    @authorize
    @validate(
        query=dict(
            max_length=(20, '702 Must Be Less Than 20 Charecters'),
            required='708 Search Query Is Required',
        )
    )
    @json
    @User.expose
    def search(self):
        query = context.form.get('query') \
            if context.form.get('query') \
            else context.query.get('query')

        query = f'%{query}%'
        query = DBSession.query(User) \
            .filter(or_(
                User.title.ilike(query),
                User.email.ilike(query)
            ))
        if not query.count():
            raise HTTPStatus('611 User Not Found')

        return query

    @authorize
    @json
    @User.expose
    def get(self, id):
        try:
            id = int(id)
        except ValueError:
            raise HTTPNotFound()

        user = DBSession.query(User).filter(User.id == id).one_or_none()
        if user is None:
            raise HTTPNotFound()

        return user

