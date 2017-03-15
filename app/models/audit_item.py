# -*- coding: utf-8 -*-

"""

    zhifang.app.models.item
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 02/27/17

"""


from sqlalchemy.dialects.mysql import MEDIUMBLOB

from . import db, AppModel


class AuditItem(AppModel):

    attachment = db.Column(MEDIUMBLOB())

    audit_item_type = db.Column(db.String(9), nullable=0)

    audit_id = db.Column(db.Integer(), db.ForeignKey("audit.id"))

    create_user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    create_user = db.relationship("User", foreign_keys=create_user_id)

    __mapper_args__ = {"polymorphic_identity": "audit_item", "polymorphic_on": audit_item_type}
