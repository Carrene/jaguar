from nanohttp import RestController, json, context, HTTPBadRequest
from restfulpy.logging_ import get_logger


logger = get_logger('auth')


class TokensController(RestController):

    @json
    def create(self):
        email = context.form.get('email')
        password = context.form.get('password')

        def bad():
            logger.info('Login failed: %s' % email)
            raise HTTPBadRequest('Invalid email or password')

        if not (email and password):
            bad()

        logger.info('Trying to login: %s' % email)
        principal = context.application.__authenticator__.\
            login((email, password))
        if principal is None:
            bad()

        return dict(token=principal.dump())


