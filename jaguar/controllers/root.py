from nanohttp import Controller, json
from restfulpy.controllers import RootController

import jaguar


class ApiV1(Controller):

    @json
    def version(self):
        return {
            'version': jaguar.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()

