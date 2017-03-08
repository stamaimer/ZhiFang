# -*- coding: utf-8 -*-

"""

    zhifang.app.models.leave
    ~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 02/27/17

"""


from . import db
from .audit_item import AuditItem


class Leave(AuditItem):

    __mapper_args__ = {"polymorphic_identity": u"请假"}

    id = db.Column(db.Integer(), db.ForeignKey("audit_item.id"), primary_key=True)

    leave_type_id = db.Column(db.Integer(), db.ForeignKey("leave_type.id"))

    leave_type = db.relationship("LeaveType", foreign_keys=leave_type_id)

    notation = db.Column(db.Text())

    beg_date = db.Column(db.Date())

    end_date = db.Column(db.Date())

    last = db.Column(db.Integer())

    def __init__(self, create_user_id, audit_id, leave_type_id, beg_date, end_date, notation, last):

        self.create_user_id = create_user_id

        self.leave_type_id = leave_type_id

        self.beg_date = beg_date

        self.end_date = end_date

        self.notation = notation

        self.audit_id = audit_id

        self.last = last
