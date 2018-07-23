
from nanohttp import RestController, json, context, HTTPBadRequest, validate


class TokensController(RestController):

    @validate(
        email=dict(
            required=(True, '400 Invalid email and password')
        )
    )
    @json
    def create(self):
        email = context.form.get('email')
        password = context.form.get('password')

        principal = context.application.__authenticator__.\
            login((email, password))
        if principal is None:
            raise HTTPBadRequest('Invalid email or password')

        return dict(token=principal.dump())

