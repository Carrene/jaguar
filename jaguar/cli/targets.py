from nanohttp import settings
from easycli import SubCommand, Argument
from restfulpy.orm import DBSession

from ..models import Target


class TargetListLauncher(SubCommand):  # pragma: no cover
    __help__ = 'List targets.'
    __command__ = 'list'

    def __call__(self, args):
        for m in DBSession.query(Target):
            print(m)


class TargetLauncher(SubCommand):  # pragma: no cover
    __help__ = 'Manage targets.'
    __command__ = 'target'
    __arguments__ = [
        TargetListLauncher,
    ]

