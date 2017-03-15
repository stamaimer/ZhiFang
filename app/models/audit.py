# -*- coding: utf-8 -*-

"""

    zhifang.app.models.audit
    ~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/01/17

"""


from . import db, AppModel
from .audit_view import AuditView


class Audit(AppModel):

    audit_items = db.relationship("AuditItem", backref="audit")

    audit_views = db.relationship("AuditView", foreign_keys=AuditView.audit_id, backref="audit", post_update=1)

    current_id = db.Column(db.Integer(), db.ForeignKey("audit_view.id"))

    current = db.relationship("AuditView", foreign_keys=current_id, uselist=0)

    status = db.Column(db.Enum(u"审批中", u"已驳回", u"已通过"), default=u"审批中")

    create_user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    create_user = db.relationship("User", foreign_keys=create_user_id)

    type = db.Column(db.Enum(u"请假", u"工时", u"报销", u"借款"))

    def __repr__(self):

        return self.status
