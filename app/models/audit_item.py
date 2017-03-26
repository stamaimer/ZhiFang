# -*- coding: utf-8 -*-

"""

    zhifang.app.models.item
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 02/27/17

"""


from . import db, AppModel


class AuditItem(AppModel):

    type = db.Column(db.String(9), nullable=0)

    create_user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    create_user = db.relationship("User", foreign_keys=create_user_id)

    status = db.Column(db.Enum(u"审批中", u"已驳回", u"已通过"), default=u"审批中")

    current_audit_view_id = db.Column(db.Integer(), db.ForeignKey("audit_view.id"))

    current_audit_view = db.relationship("AuditView", foreign_keys=current_audit_view_id, uselist=0, cascade="all,delete")

    __mapper_args__ = {"polymorphic_identity": "audit_item", "polymorphic_on": type}
