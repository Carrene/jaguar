
from typing import Union
from sqlalchemy import or_

import itsdangerous
from nanohttp import json, context, HTTPStatus, settings, validate
from restfulpy.controllers import ModelRestController
from restfulpy.logging_ import get_logger
from restfulpy.orm import DBSession

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

    @validate(
        search_string=dict(
            max_length=(20, '702 Must Be Less Than 20 Charecters')
        )
    )
    @json
    @User.expose
    def search(self):
        search_string = f'%{context.form.get("search_string")}%'
        query = DBSession.query(User) \
            .filter(or_(
                User.title.ilike(search_string),
                User.email.ilike(search_string)
            ))
        if not query.count():
            raise HTTPStatus('611 User Not Found')

        return query

