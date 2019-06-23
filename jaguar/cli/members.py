from nanohttp import settings
from easycli import SubCommand, Argument
from restfulpy.orm import DBSession

from ..models import Member


class MemberListLauncher(SubCommand):  # pragma: no cover
    __help__ = 'List members.'
    __command__ = 'list'

    def __call__(self, args):
        for m in DBSession.query(Member):
            print(m)


class MemberLauncher(SubCommand):  # pragma: no cover
    __help__ = 'Mamage member.'
    __command__ = 'member'
    __arguments__ = [
        MemberListLauncher,
    ]

