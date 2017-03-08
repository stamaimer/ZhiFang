# -*- coding: utf-8 -*-

"""

    zhifang.app.models.project
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 02/27/17

"""


from . import db, AppModel


class Project(AppModel):

    no = db.Column(db.String(128))

    name = db.Column(db.String(128), unique=1)

    region_id = db.Column(db.Integer(), db.ForeignKey("region.id"))

    region = db.relationship("Region", foreign_keys=region_id, backref="projects")

    charge_user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    charge_user = db.relationship("User", foreign_keys=charge_user_id)

    current_stage_id = db.Column(db.Integer(), db.ForeignKey("project_stage.id"))

    current_stage = db.relationship("ProjectStage", foreign_keys=current_stage_id)

    def __repr__(self):

        return self.name