# -*- coding: utf-8 -*-

"""

    zhifang.app.models.bulletin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/07/17

"""


from . import db, AppModel


class Bulletin(AppModel):

    title = db.Column(db.String(255))

    content = db.Column(db.Text())
