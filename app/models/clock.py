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

    position = db.Column(db.Text())

    datetime = db.Column(db.DateTime(), default=func.now())

    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"))

    project = db.relationship("Project", foreign_keys=project_id)

    create_user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    create_user = db.relationship("User", foreign_keys=create_user_id)

    def __init__(self, notation, position, project_id, create_user_id):

        self.create_user_id = create_user_id

        self.project_id = project_id

        self.notation = notation

        self.position = position

    def __repr__(self):

        return self.create_user.username + u" 在 " + self.position + u" 于 " + self.datetime + u" 打卡"
