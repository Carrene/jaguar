from nanohttp import json, context
from restfulpy.controllers import ModelRestController
from ..models import Envelop, Message


class MessageController(ModelRestController):
    __model__ = Envelop

    def __init__(self, target):
         self.target = target

    @json
    @Message.expose
    def send(self):
        body = context.form.get('body')
        type = context.form.get('type')
        message = Message(body=body, type=type)
        return message


