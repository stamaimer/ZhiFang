# -*- coding: utf-8 -*-

"""

    zhifang.app.models.reimbursement
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/04/17

"""


from sqlalchemy.dialects.mysql import MEDIUMBLOB

from . import db
from .audit_item import AuditItem


class Reimbursement(AuditItem):

    __mapper_args__ = {"polymorphic_identity": u"报销"}

    id = db.Column(db.Integer(), db.ForeignKey("audit_item.id"), primary_key=1)

    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"))

    project = db.relationship("Project", foreign_keys=project_id)

    reimbursement_type_id = db.Column(db.Integer(), db.ForeignKey("reimbursement_type.id"))

    reimbursement_type = db.relationship("ReimbursementType", foreign_keys=reimbursement_type_id)

    amount = db.Column(db.Float())

    notation = db.Column(db.Text())

    attachment = db.Column(MEDIUMBLOB())

    def __init__(self, create_user_id, attachment, project_id, reimbursement_type_id, notation, amount):

        self.reimbursement_type_id = reimbursement_type_id

        self.create_user_id = create_user_id

        self.project_id = project_id

        self.attachment = attachment

        self.notation = notation

        self.amount = amount
