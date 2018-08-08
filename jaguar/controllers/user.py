
from sqlalchemy import or_
import itsdangerous
from nanohttp import json, context, HTTPStatus, settings, validate
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession
from restfulpy.authorization import authorize

from jaguar.models import User


class UserController(ModelRestController):
    __model__ = User

    @json
    def register(self):
        serializer = \
            itsdangerous.URLSafeTimedSerializer(settings.activation.secret)
        try:
            email = serializer.loads(
                context.form.get('token'),
                max_age=settings.activation.max_age,
            )
        except itsdangerous.BadSignature:
            raise HTTPStatus(status='703 Invalid email activation token')
        user = User(
            email=email,
            title=context.form.get('title'),
            password=context.form.get('password')
        )
        user.is_active = True
        DBSession.add(user)
        DBSession.commit()
        principal = user.create_jwt_principal()
        context.response_headers.add_header(
            'X-New-JWT-Token',
            principal.dump().decode('utf-8')
        )
        return user

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

