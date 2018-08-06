
from nanohttp import json, context, validate, HTTPStatus
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from jaguar.models import User, contact


class ContactController(ModelRestController):
    __model__ = User

    @authorize
    @validate(
        userId=dict(
            type_=(int, '705 Invalid User Id'),
            required=(True, '709 User Id Is Required'),
        )
    )
    @json
    @User.expose
    @commit
    def add(self):
        source = User.current()
        user_id = context.form.get('userId')
        destination = DBSession.query(User) \
        .filter(User.id == user_id).one_or_none()
        if destination is None:
            raise HTTPStatus('611 User Not Found')

        is_contact = DBSession.query(contact) \
            .filter(
                contact.c.source == context.identity.id,
                contact.c.destination == user_id
            ).count()
        if is_contact:
            raise HTTPStatus('603 Already Added To Contacts')

        source.contacts.append(destination)
        return source

