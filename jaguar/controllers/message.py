import io
from nanohttp import json, context, HTTPStatus, validate, HTTPForbidden, \
    HTTPBadRequest
from restfulpy.authorization import authorize
from restfulpy.orm import commit, DBSession
from restfulpy.controllers import ModelRestController
from sqlalchemy_media import store_manager

from ..models import Envelop, Message, TargetMember, User, Target


SUPPORTED_MIME_TYPES=['text/plain', 'image/jpeg', 'image/png', 'image/jpg',]


class MessageController(ModelRestController):
    __model__ = Message

    @store_manager(DBSession)
    @authorize
    @validate(
        body=dict(
            max_length=(1024, '702 Must be less than 1024 charecters'),
            required='400 Bad Request',
        ),
        replyTo=dict(type_=(int, '707 Invalid MessageId'))
    )
    @json
    @Message.expose
    @commit
    def send(self, target_id):
        body = context.form.get('body')
        mimetype = context.form.get('mimetype')
        attachment = context.form.get('attachment')
        if not mimetype in SUPPORTED_MIME_TYPES:
            raise HTTPStatus('415 Unsupported Media Type')

        current_member = DBSession.query(User) \
            .filter(User.reference_id == context.identity.reference_id) \
            .one()
        is_member = DBSession.query(TargetMember) \
            .filter(
                TargetMember.target_id == target_id,
                TargetMember.member_id == current_member.id
            ) \
            .count()
        if not is_member:
            raise HTTPForbidden()

        message = Message(body=body, mimetype=mimetype)
        message.target_id = target_id
        message.sender_id = current_member.id
        if 'replyTo' in context.form:
            requested_message = DBSession.query(Message) \
                .filter(Message.id == context.form.get('replyTo')) \
                .one_or_none()
            if requested_message is None:
                raise HTTPStatus('614 Message Not Found')

            if requested_message.is_deleted:
                raise HTTPStatus('616 Message Already Deleted')

            message.reply_to = requested_message

        if 'attachment' in context.form:
            message.attachment = attachment

            if message.attachment.content_type != mimetype:
                raise HTTPStatus(
                    '710 The Mimetype Does Not Match The File Type'
                )

        DBSession.add(message)
        return message

    @authorize
    @json(prevent_form='711 Form Not Allowed')
    @Message.expose
    def list(self, target_id):
        current_member = DBSession.query(User) \
            .filter(User.reference_id == context.identity.reference_id) \
            .one()
        is_member = DBSession.query(TargetMember) \
            .filter(
                TargetMember.target_id == target_id,
                TargetMember.member_id == current_member.id
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

        if message.is_deleted:
            raise HTTPStatus('616 Message Already Deleted')

        current_member = DBSession.query(User) \
            .filter(User.reference_id == context.identity.reference_id) \
            .one()
        is_member = DBSession.query(TargetMember) \
            .filter(
                TargetMember.target_id == message.target_id,
                TargetMember.member_id == current_member.id
            ) \
            .count()
        if not is_member:
            raise HTTPForbidden()

        message.body = 'This message is deleted'
        message.mimetype = 'text/plain'
        message.soft_delete()
        return message

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
    def edit(self, id):
        try:
            id = int(id)
        except ValueError:
            raise HTTPStatus('707 Invalid MessageId')

        new_message_body = context.form.get('body')
        current_member = DBSession.query(User) \
            .filter(User.reference_id == context.identity.reference_id) \
            .one()
        message = DBSession.query(Message) \
            .filter(Message.id == id) \
            .one_or_none()
        if message is None:
            raise HTTPStatus('614 Message Not Found')

        if message.is_deleted:
            raise HTTPStatus('616 Message Already Deleted')

        if message.sender_id != current_member.id:
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

        current_user = DBSession.query(User) \
            .filter(User.reference_id == context.identity.reference_id) \
            .one()
        is_subscribe = DBSession.query(Target) \
            .filter(
                Target.id == message.target_id,
                TargetMember.target_id == message.target_id,
                TargetMember.member_id == current_user.id
            ) \
            .count()
        if not is_subscribe:
            raise HTTPForbidden()

        return message

