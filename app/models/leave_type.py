# -*- coding: utf-8 -*-

"""

    zhifang.app.models.leave_type
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/03/17

"""


from . import db, AppModel


class LeaveType(AppModel):

    text = db.Column(db.String(9), unique=1)

    def __init__(self, text=""):

        self.text = text

    def __repr__(self):

        return self.text
