from restfulpy.authentication import StatefulAuthenticator


class Authenticator(StatefulAuthenticator):
    def create_principal(self, **kwargs):
        pass

    # noinspection PyUnresolvedReferences
    def create_refresh_principal(self):
        pass

    # noinspection PyUnresolvedReferences
    def validate_credentials(self):
        pass
