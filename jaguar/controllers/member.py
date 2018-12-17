
from sqlalchemy import or_
from nanohttp import json, context, HTTPStatus, settings, validate, \
    HTTPNotFound, HTTPBadRequest
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit
from restfulpy.authorization import authorize

from ..models import Member
from ..validators import search_member_validator, create_member_validator


class MemberController(ModelRestController):
    __model__ = Member

    @authorize
    @search_member_validator
    @json
    @Member.expose
    def search(self):
        query = context.form.get('query') \
            if context.form.get('query') \
            else context.query.get('query')

        query = f'%{query}%'
        query = DBSession.query(Member) \
            .filter(or_(
                Member.title.ilike(query),
                Member.email.ilike(query)
            ))
        if not query.count():
            raise HTTPStatus('611 Member Not Found')

        return query

    @authorize
    @json
    @Member.expose
    def get(self, id):
        try:
            id = int(id)
        except ValueError:
            raise HTTPNotFound()

        user = DBSession.query(Member).filter(Member.id == id).one_or_none()
        if user is None:
            raise HTTPNotFound()

        return user

    @authorize
    @json
    @Member.expose
    @commit
    def ensure(self):
        if not 'HTTP_X_OAUTH2_ACCESS_TOKEN' in context.environ:
            raise HTTPBadRequest()

        access_token = context.environ['HTTP_X_OAUTH2_ACCESS_TOKEN']

        member = DBSession.query(Member) \
            .filter(Member.reference_id == context.identity.reference_id) \
            .one_or_none()

        if not member:
            member = Member(
                email=context.identity.email,
                title=context.identity.payload['title'],
                reference_id=context.identity.reference_id,
                access_token=access_token
            )
            DBSession.add(member)
        else:
            member.access_token = access_token

        DBSession.add(member)
        return member

