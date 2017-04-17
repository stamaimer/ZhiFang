# -*- coding: utf-8 -*-

"""

    zhifang.app.models.loan
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/04/17

"""


from sqlalchemy.dialects.mysql import MEDIUMBLOB

from . import db
from .audit_item import AuditItem


class Loan(AuditItem):

    __mapper_args__ = {"polymorphic_identity": u"借款"}

    id = db.Column(db.Integer(), db.ForeignKey("audit_item.id"), primary_key=1)

    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"))

    project = db.relationship("Project", foreign_keys=project_id)

    printed = db.Column(db.Enum(u"已打印", u"未打印"), default=u"未打印")

    amount = db.Column(db.Float())

    notation = db.Column(db.Text())

    attachment = db.Column(MEDIUMBLOB())

    def __init__(self, create_user_id, attachment, project_id, notation, amount):

        self.create_user_id = create_user_id

        self.project_id = project_id

        self.attachment = attachment

        self.notation = notation

        self.amount = amount
