# -*- coding: utf-8 -*-

"""

    zhifang.app.models.work_content
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/03/17

"""


from . import db, AppModel


class WorkType(AppModel):

    text = db.Column(db.String(9), unique=True, nullable=False)

    def __init__(self, text=""):

        self.text = text

    def __repr__(self):

        return self.text
