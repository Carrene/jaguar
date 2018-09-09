from restfulpy.controllers import RestController
from .token import TokenController

class OAUTHController(RestController):
    def __call__(self, *remaining_paths):
        if len(remaining_paths) and remaining_paths[0] == 'tokens':
            return TokenController()(*remaining_paths[1:])

