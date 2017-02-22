# -*- coding: utf-8 -*-

"""

    zhifang.app.models.role
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 02/22/17

"""


from flask_security import RoleMixin

from . import db


class Role(db.Model, RoleMixin):

    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(128), unique=True)

    description = db.Column(db.String(128))

    def __init__(self, name="", description=""):

        self.name = name

        self.description = description

    def __repr__(self):

        return self.name
