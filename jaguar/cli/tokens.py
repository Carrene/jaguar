import sys

from easycli import SubCommand, Argument
from restfulpy.orm import DBSession

from ..models import Member


class CreateTokenSubSubCommand(SubCommand):
    __help__ = 'Create a jwt token.'
    __command__ = 'create'
    __arguments__ = [
        Argument(
            'member_id',
            type=int,
            help='Member id',
        ),
        Argument(
            'access_token',
            type=str,
            help='Access token',
        ),
    ]

    def __call__(self, args):
        member = DBSession.query(Member)\
            .filter(Member.id == args.member_id)\
            .one_or_none()

        if member is None:
            print(f'Invalid member id: {self.args.member_id}', file=sys.stderr)
            return 1

        member.access_token = args.access_token
        DBSession.commit()

        token = member.create_jwt_principal()
        print(token.dump().decode())


class TokenSubCommand(SubCommand):
    __help__ = 'Token related.'
    __command__ = 'token'
    __arguments__ = [
        CreateTokenSubSubCommand,
    ]

