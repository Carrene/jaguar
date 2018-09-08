
from nanohttp import RestController, json, context, HTTPBadRequest, validate
from restfulpy.authorization import authorize


class TokenController(RestController):

    @validate(
        email=dict(required='400 Invalid email or password')
    )
    @json
    def create(self):
        email = context.form.get('email')
        principal = context.application.__authenticator__.login(email)
        if principal is None:
            raise HTTPBadRequest('Invalid email or password')
        return dict(token=principal.dump())

    @authorize
    @json
    def invalidate(self):
        context.application.__authenticator__.logout()
        return {}

