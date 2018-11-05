
from nanohttp import Controller, json, action
from restfulpy.controllers import RootController
from restfulpy.authorization import authorize

import jaguar

from .member import MemberController
from .email import EmailController
from .token import TokenController
from .room import RoomController
from .target import TargetController
from .contact import ContactController
from .direct import DirectController
from .message import MessageController
from .oauth2 import OAUTHController
from .subscribetarget import SubscribeTargetController


class ApiV1(Controller):

    members = MemberController()
    emails = EmailController()
    tokens = TokenController()
    rooms = RoomController()
    targets = TargetController()
    contacts = ContactController()
    directs = DirectController()
    messages = MessageController()
    oauth2 = OAUTHController()
    subscribetargets = SubscribeTargetController()

    @json
    def version(self):
        return {
            'version': jaguar.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()

