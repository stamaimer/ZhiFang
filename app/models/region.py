# -*- coding: utf-8 -*-

"""

    zhifang.app.models.region
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 02/23/17

"""


from . import db, AppModel


class Region(AppModel):

    text = db.Column(db.String(128), unique=1, nullable=0)

    status = db.Column(db.Boolean(), default=1)

    charge_user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=0)

    charge_user = db.relationship("User", foreign_keys=charge_user_id)

    def __init__(self, text="", charge_user=None):

        self.text = text

        self.charge_user = charge_user

    def __repr__(self):

        return self.text
