
from nanohttp import json, context, validate, HTTPStatus
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from jaguar.models import User, Contact


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
        user_id = context.form.get('userId')
        destination = DBSession.query(User) \
        .filter(User.id == user_id).one_or_none()
        if destination is None:
            raise HTTPStatus('611 User Not Found')

        is_contact = DBSession.query(Contact) \
            .filter(
                Contact.source == context.identity.id,
                Contact.destination == user_id
            ).count()
        if is_contact:
            raise HTTPStatus('603 Already Added To Contacts')

        DBSession.add(Contact(source=context.identity.id, destination=user_id))

        return User.current()

