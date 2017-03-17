# -*- coding: utf-8 -*-

"""

    zhifang.app.models.clock
    ~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 02/27/17

"""


from sqlalchemy.sql import func

from . import db, AppModel


class Clock(AppModel):

    notation = db.Column(db.Text())

    position = db.Column(db.Text(), nullable=0)

    datetime = db.Column(db.DateTime(), default=func.now())

    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"), nullable=0)

    project = db.relationship("Project", foreign_keys=project_id)

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=0)

    user = db.relationship("User", foreign_keys=user_id)

    def __init__(self, notation, position, project_id, user_id):

        self.notation = notation

        self.position = position

        self.project_id = project_id

        self.user_id = user_id

    def __repr__(self):

        return self.user.username + u" 在 " + self.position + u" 于 " + self.datetime + u" 打卡"
