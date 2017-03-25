# -*- coding: utf-8 -*-

"""

    zhifang.app.models.bulletin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/07/17

"""


from sqlalchemy.event import listens_for

from app.utilities import push

from . import db, bulletins_users, AppModel


class Bulletin(AppModel):

    content = db.Column(db.Text())

    title = db.Column(db.String(255))

    image = db.Column(db.String(999))

    status = db.Column(db.Boolean(), default=1)

    authorized_users = db.relationship("User", secondary=bulletins_users)


@listens_for(Bulletin, "after_insert")
def push_after_insert(mapper, connection, target):

    push(u"你有一条新的通知公告：%s" % target.title, *[user.registration_id for user in target.authorized_users])


@listens_for(Bulletin.status, "set")
def push_after_status_set(target, value, oldvalue, initiator):
    if not oldvalue and value:
        push(u"你有一条新的通知公告：%s" % target.title, *[user.registration_id for user in target.authorized_users])
