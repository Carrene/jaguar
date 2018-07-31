
from nanohttp import Controller, json
from restfulpy.controllers import RootController

import jaguar

from .member import MemberController
from .email import EmailController
from .token import TokenController
from .room import RoomController


class ApiV1(Controller):

    members = MemberController()
    emails = EmailController()
    tokens = TokenController()
    rooms = RoomController()

    @json
    def version(self):
        return {
            'version': jaguar.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()

