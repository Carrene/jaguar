
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession
from nanohttp import json, context

from jaguar.models import Target, Room

class RoomsController(ModelRestController):
    __model__ = Target

    @json
    def create(self):
        title = context.form.get('title')
        room = Room(title = title)
        DBSession.add(room)

        return room

