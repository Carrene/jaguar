import itsdangerous
from easycli import SubCommand, Argument
from nanohttp import settings

from jaguar.models import ActivationEmail


class SendEmailSubSubCommand(SubCommand):  # pragma: no cover
    __help__ = 'Sends an email.'
    __command__ = 'send'
    __arguments__ = [
        Argument(
            '-e',
            '--email',
            required=True,
            help='Email to be claim',
        ),
    ]

    def __call__(self, args):

        serializer = \
            itsdangerous.URLSafeTimedSerializer(settings.activation.secret)

        token = serializer.dumps(args.email)

        email = ActivationEmail(
                to=args.email,
                subject='Activate your Cucumber account',
                body={
                    'activation_token': token,
                    'activation_url': settings.activation.url
                }
        )
        email.to = args.email
        email.do_({})


class EmailSubCommand(SubCommand):  # pragma: no cover
    __help__ = 'Manage emails.'
    __command__ = 'email'
    __arguments__ = [
        SendEmailSubSubCommand,
    ]

