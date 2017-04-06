# -*- coding: utf-8 -*-

"""

    zhifang.app.models.audit_view

    stamaimer 03/01/17

"""


from sqlalchemy.event import listens_for

from app.utilities import push

from . import db, AppModel


class AuditView(AppModel):

    next_id = db.Column(db.Integer(), db.ForeignKey("audit_view.id"))

    _next_ = db.relationship("AuditView", remote_side="AuditView.id", backref=db.backref("last", uselist=0), uselist=0,
                             post_update=1)

    advice = db.Column(db.Text())

    status = db.Column(db.Boolean(), default=0)

    result = db.Column(db.Enum(u"同意", u"驳回", u"转审"))

    audit_user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    audit_user = db.relationship("User", foreign_keys=audit_user_id)

    audit_item_id = db.Column(db.Integer(), db.ForeignKey("audit_item.id"))

    audit_item = db.relationship("AuditItem", foreign_keys=audit_item_id)

    def __repr__(self):

        if self.result:

            if self.result == u"转审":

                return self.audit_user.username + u"\t已于 " + self.update_datetime.__str__() + ' ' \
                       + self.result + u" 给 " + self._next_.audit_user.username + "\t" + self.advice
            else:

                return self.audit_user.username + u"\t已于 " + self.update_datetime.__str__() + ' ' \
                       + self.result + "\t" + (self.advice if self.advice else "")

        else:

            return u"等待 " + self.audit_user.username + u" 审批"


@listens_for(AuditView, "after_insert")
def push_after_insert(mapper, connection, target):
    if target.status:
        push(u"你有一条来自{}的{}申请".format(target.audit_item.create_user.username, target.audit_item.type),
             target.audit_user.registration_id)


@listens_for(AuditView.status, "set")
def push_after_status_set(target, value, oldvalue, initiator):
    if not oldvalue and value:
        push(u"你有一条来自{}的{}申请".format(target.audit_item.create_user.username, target.audit_item.type),
             target.audit_user.registration_id)


@listens_for(AuditView.result, "set")
def push_after_result_set(target, value, oldvalue, initiator):
    if value:
        push(u"{}已经{}你的{}申请".format(target.audit_user.username, value, target.audit_item.type),
             target.audit_item.create_user.registration_id)
