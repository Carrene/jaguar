from nanohttp import json, context, HTTPStatus, validate, HTTPForbidden
from restfulpy.authorization import authorize
from restfulpy.orm import commit, DBSession
from restfulpy.controllers import ModelRestController

from ..models import Envelop, Message, target_member


SUPPORTED_MIME_TYPES=['text/plain']


class MessageController(ModelRestController):
    __model__ = Envelop

    @authorize
    @validate(
        body=dict(
            max_length=(1024, '702 Must be less than 1024 charecters'),
            required='400 Bad Request',
        )
    )
    @json
    @Message.expose
    @commit
    def send(self, target_id):
        body = context.form.get('body')
        mime_type = context.form.get('mimeType')
        if not mime_type in SUPPORTED_MIME_TYPES:
            raise HTTPStatus('415 Unsupported Media Type')

        message = Message(body=body, mime_type=mime_type)
        message.target_id = target_id
        message.sender_id = context.identity.id
        DBSession.add(message)
        return message

    @authorize
    @json(prevent_form='711 Form Not Allowed')
    @Message.expose
    def list(self, target_id):
        is_member = DBSession.query(target_member) \
            .filter(
                target_member.c.target_id == target_id,
                target_member.c.member_id == context.identity.id
            ) \
            .count()
        if not is_member:
            raise HTTPForbidden

        query = DBSession.query(Message) \
            .filter(Message.target_id == target_id)
        return query

    @authorize
    @json
    @Message.expose
    @commit
    def delete(self, id):
        try:
            id = int(id)
        except:
            raise HTTPStatus('707 Invalid MessageId')

        message = DBSession.query(Message) \
            .filter(Message.id == id) \
            .one_or_none()
        if message is None:
            raise HTTPStatus('614 Message Not Found')

        is_member = DBSession.query(target_member) \
            .filter(
                target_member.c.target_id == message.target_id,
                target_member.c.member_id == context.identity.id
            ) \
            .count()
        if not is_member:
            raise HTTPForbidden()

        DBSession.delete(message)
        return message

