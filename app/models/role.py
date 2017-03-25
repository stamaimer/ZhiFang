# -*- coding: utf-8 -*-

"""

    zhifang.app.models.role
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 02/22/17

"""


from flask_security import RoleMixin

from . import db, AppModel


class Role(AppModel, RoleMixin):

    name = db.Column(db.String(128), unique=1, nullable=0)

    description = db.Column(db.String(128))

    def __init__(self, name="", description=""):

        self.name = name

        self.description = description

    def __repr__(self):

        return self.name
