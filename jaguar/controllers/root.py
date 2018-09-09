
from nanohttp import Controller, json
from restfulpy.controllers import RootController

import jaguar

from .user import UserController
from .email import EmailController
from .token import TokenController
from .room import RoomController
from .target import TargetController
from .contact import ContactController
from .direct import DirectController
from .message import MessageController
from .oauth2 import OAUTHController


class ApiV1(Controller):

    users = UserController()
    emails = EmailController()
    tokens = TokenController()
    rooms = RoomController()
    targets = TargetController()
    contacts = ContactController()
    directs = DirectController()
    messages = MessageController()
    oauth2 = OAUTHController()

    @json
    def version(self):
        return {
            'version': jaguar.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()

