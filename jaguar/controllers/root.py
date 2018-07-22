
from nanohttp import Controller, json
from restfulpy.controllers import RootController

import jaguar

from .members import MembersController
from .emails import EmailsController
from .tokens import TokensController
from .rooms import RoomsController


class ApiV1(Controller):

    members = MembersController()
    emails = EmailsController()
    tokens = TokensController()
    rooms = RoomsController()
    
    @json
    def version(self):
        return {
            'version': jaguar.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()

