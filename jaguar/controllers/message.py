from nanohttp import json, context, HTTPStatus, validate
from restfulpy.authorization import authorize
from restfulpy.orm import commit, DBSession
from restfulpy.controllers import ModelRestController

from ..models import Envelop, Message


SUPPORTED_MIME_TYPES=['text/plain']


class MessageController(ModelRestController):
    __model__ = Envelop

    def __init__(self, target):
         self.target = target

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
    def send(self):
        body = context.form.get('body')
        mime_type = context.form.get('mimeType')
        if not mime_type in SUPPORTED_MIME_TYPES:
            raise HTTPStatus('415 Unsupported Media Type')

        message = Message(body=body, mime_type=mime_type)
        message.target_id = self.target.id
        message.sender_id = context.identity.id
        DBSession.add(message)
        return message

    @authorize
    @json
    @Message.expose
    def list(self):
        query = DBSession.query(Message) \
            .filter(Message.target_id == self.target.id)

        return query

