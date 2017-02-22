# -*- coding: utf-8 -*-

"""

    zhifang.app.models.user
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaime 02/22/17

"""


from flask_security import UserMixin
from . import db, roles_users


class User(db.Model, UserMixin):

    id = db.Column(db.Integer(), primary_key=True)

    email = db.Column(db.String(128), unique=True)

    phone = db.Column(db.String(128), unique=True)

    active = db.Column(db.Boolean(), default=True)

    username = db.Column(db.String(128))

    password = db.Column(db.String(128))

    roles = db.relationship("Role", secondary=roles_users,
                            backref=db.backref("users", lazy="dynamic"))

    def __init__(self, email="", phone="", active="", username="", password="", roles=None):

        self.email = email

        self.phone = phone

        self.active = active

        self.username = username

        self.password = password

        self.roles = roles

    def __repr__(self):

        return self.username
