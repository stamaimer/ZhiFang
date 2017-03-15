# -*- coding: utf-8 -*-

"""

    zhifang.app.model.attendance
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/14/17

"""


from . import db, AppModel


class Attendance(AppModel):

    attendance_type = db.Column(db.String(9), nullable=0)

    notation = db.Column(db.Text())

    __mapper_args__ = {"polymorphic_identity": "attendance", "polymorphic_on": attendance_type}