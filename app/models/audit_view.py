# -*- coding: utf-8 -*-

"""

    zhifang.app.models.audit_view

    stamaimer 03/01/17

"""


from . import db, AppModel


class AuditView(AppModel):

    id = db.Column(db.Integer(), primary_key=True)

    next_id = db.Column(db.Integer(), db.ForeignKey("audit_view.id"))

    _next_ = db.relationship("AuditView", remote_side="AuditView.id", backref=db.backref("last", uselist=0), uselist=0,
                             post_update=1)

    advice = db.Column(db.Text())

    status = db.Column(db.Boolean(), default=0)

    result = db.Column(db.Enum(u"同意", u"驳回", u"转审"))

    audit_user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    audit_user = db.relationship("User", foreign_keys=audit_user_id)

    audit_id = db.Column(db.Integer(), db.ForeignKey("audit.id"))

    def __repr__(self):

        return self.audit_user.username
