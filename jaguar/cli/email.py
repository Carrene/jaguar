import itsdangerous
from nanohttp import settings
from easycli import SubCommand, Argument

from jaguar.models import ActivationEmail


class SendEmailLauncher(SubCommand):  # pragma: no cover
    __help__ = 'Sends an email.'
    __command__ = 'send'
    __arguments__ = [
        Argument(
            '-e',
            '--email',
            required=True,
            help='Email to be claim'
        ),
    ]

    def __call__(self, args):

        serializer = \
            itsdangerous.URLSafeTimedSerializer(settings.activation.secret)

        token = serializer.dumps(self.args.email)

        email = ActivationEmail(
                to=self.args.email,
                subject='Activate your Cucumber account',
                body={
                    'activation_token': token,
                    'activation_url': settings.activation.url
                }
        )
        email.to = self.args.email
        email.do_({})


class EmailLauncher(SubCommand):  # pragma: no cover
    __help__ = 'Manage emails.'
    __command__ = 'email'
    __arguments__ = [
        SendEmailLauncher,
    ]

