from nanohttp import Controller, json
from restfulpy.controllers import RootController

from jaguar.controllers.members import MembersController

import jaguar


class ApiV1(Controller):

    import pudb; pudb.set_trace()  # XXX BREAKPOINT
    members = MembersController()

    @json
    def version(self):
        return {
            'version': jaguar.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()
