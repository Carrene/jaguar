from restfulpy.authorization import authorize
from restfulpy.orm import commit, DBSession
from restfulpy.controllers import ModelRestController
from sqlalchemy_media import store_manager
from nanohttp import json, context, HTTPStatus, validate, HTTPForbidden, \
    settings

from ..messaging.queues import queue_manager
from ..models import Envelop, Message, TargetMember, Member, Target
from ..validators import send_message_validator, edit_message_validator, \
    reply_message_validator


SUPPORTED_MIME_TYPES=['text/plain', 'image/jpeg', 'image/png', 'image/jpg',]


class MessageController(ModelRestController):
    __model__ = Message

    @store_manager(DBSession)
    @authorize
    @send_message_validator
    @json
    @Message.expose
    def send(self, target_id):
        body = context.form.get('body')
        mimetype = context.form.get('mimetype')
        attachment = context.form.get('attachment')
        if not mimetype in SUPPORTED_MIME_TYPES:
            raise HTTPStatus('415 Unsupported Media Type')

        message = Message(body=body, mimetype=mimetype)
        message.target_id = int(target_id)
        message.sender_id = Member.current().id
        if 'attachment' in context.form:
            message.attachment = attachment

            if message.attachment.content_type != mimetype:
                raise HTTPStatus(
                    '710 The Mimetype Does Not Match The File Type'
                )

        DBSession.add(message)
        DBSession.flush()

        try:
            queue_manager.enqueue(
                settings.rabbitmq.worker_queue, message.to_dict()
            )
        except:
            raise

        # After consulting with Mr.Mardani, the result got to remove `commit`
        # decorator and use `commit()` straightly instead. It's cause of
        # enqueueing the message to `workers`(queue) must be applied after
        # commit
        DBSession.commit()
        return message

    @authorize
    @store_manager(DBSession)
    @json(prevent_form='711 Form Not Allowed')
    @Message.expose
    def list(self, target_id):
        query = DBSession.query(Message) \
            .filter(Message.target_id == target_id)
        return query

    @authorize
    @store_manager(DBSession)
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

        if message.is_deleted:
            raise HTTPStatus('616 Message Already Deleted')

        if not message.sender_id == Member.current().id:
            raise HTTPForbidden()

        message.body = 'This message is deleted'
        message.mimetype = 'text/plain'
        message.soft_delete()

        DBSession.flush()

        try:
            queue_manager.enqueue(
                settings.rabbitmq.worker_queue, message.to_dict()
            )
        except:
            raise

        return message

    @authorize
    @edit_message_validator
    @json
    @Message.expose
    @commit
    def edit(self, id):
        try:
            id = int(id)
        except ValueError:
            raise HTTPStatus('707 Invalid MessageId')

        new_message_body = context.form.get('body')
        message = DBSession.query(Message) \
            .filter(Message.id == id) \
            .one_or_none()
        if message is None:
            raise HTTPStatus('614 Message Not Found')

        if message.is_deleted:
            raise HTTPStatus('616 Message Already Deleted')

        if message.sender_id != Member.current().id:
            raise HTTPForbidden()

        message.body = new_message_body
        DBSession.add(message)
        return message

    @authorize
    @json
    @Message.expose
    def get(self, id):
        try:
            id = int(id)
        except(ValueError, TypeError):
            raise HTTPStatus('707 Invalid Message Id')

        message = DBSession.query(Message) \
            .filter(Message.id == id) \
            .one_or_none()
        if message is None:
            raise HTTPStatus('614 Message Not Found')

        is_subscribe = DBSession.query(Target) \
            .filter(
                Target.id == message.target_id,
                TargetMember.target_id == message.target_id,
                TargetMember.member_id == Member.current().id
            ) \
            .count()
        if not is_subscribe:
            raise HTTPForbidden()

        return message

    @authorize
    @reply_message_validator
    @json
    @Message.expose
    @commit
    def reply(self, message_id):
        try:
            message_id = int(message_id)
        except(ValueError, TypeError):
            raise HTTPStatus('707 Invalid MessageId')

        mimetype = context.form.get('mimetype')
        if not mimetype in SUPPORTED_MIME_TYPES:
            raise HTTPStatus('415 Unsupported Media Type')

        requested_message = DBSession.query(Message) \
            .filter(Message.id == message_id) \
            .one_or_none()
        if requested_message is None:
            raise HTTPStatus('614 Message Not Found')

        if requested_message.is_deleted:
            raise HTTPStatus('616 Message Already Deleted')

        message = Message(body=context.form.get('body'), mimetype=mimetype)
        message.target_id = requested_message.target_id
        message.sender_id = Member.current().id
        message.reply_to = requested_message
        DBSession.add(message)
        return message

