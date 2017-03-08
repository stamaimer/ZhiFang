# -*- coding: utf-8 -*-

"""

    zhifang.app.models.work
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/02/17

"""


from . import db
from .audit_item import AuditItem


class Work(AuditItem):

    __mapper_args__ = {"polymorphic_identity": u"工时"}

    id = db.Column(db.Integer(), db.ForeignKey("audit_item.id"), primary_key=True)

    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"))

    project = db.relationship("Project", foreign_keys=project_id)

    project_stage_id = db.Column(db.Integer(), db.ForeignKey("project_stage.id"))

    project_stage = db.relationship("ProjectStage", foreign_keys=project_stage_id)

    specialty_id = db.Column(db.Integer(), db.ForeignKey("specialty.id"))

    specialty = db.relationship("Specialty", foreign_keys=specialty_id)

    work_type_id = db.Column(db.Integer(), db.ForeignKey("work_type.id"))

    work_type = db.relationship("WorkType", foreign_keys=work_type_id)

    date = db.Column(db.Date())

    hour = db.Column(db.Float())

    notation = db.Column(db.Text())

    def __init__(self, create_user_id, audit_id,
                 project_id, project_stage_id, specialty_id, work_type_id, notation, date, hour):

        self.project_stage_id = project_stage_id

        self.create_user_id = create_user_id

        self.specialty_id = specialty_id

        self.work_type_id = work_type_id

        self.project_id = project_id

        self.audit_id = audit_id

        self.notation = notation

        self.date = date

        self.hour = hour

