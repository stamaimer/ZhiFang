# -*- coding: utf-8 -*-

"""

    zhifang.app.models.specialty
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 02/23/17

"""


from . import db, AppModel


class Specialty(AppModel):

    text = db.Column(db.String(128), unique=1)

    def __init__(self, text=""):

        self.text = text

    def __repr__(self):

        return self.text

