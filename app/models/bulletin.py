# -*- coding: utf-8 -*-

"""

    zhifang.app.models.bulletin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/07/17

"""


from sqlalchemy.event import listens_for

from app.utilities import push

from . import db, bulletins_users, AppModel
from .user import User


class Bulletin(AppModel):

    content = db.Column(db.Text(), nullable=0)

    title = db.Column(db.String(255), nullable=0)

    image = db.Column(db.String(999))

    status = db.Column(db.Boolean(), default=1)

    authorized_users = db.relationship("User", secondary=bulletins_users)


@listens_for(Bulletin, "after_insert")
def push_after_insert(mapper, connection, target):

    if not target.authorized_users:

        for user in User.query.filter(User.roles.any(name="general")).all():
            connection.execute(
                bulletins_users.insert().values(bulletin_id=target.id, user_id=user.id)
            )

    push(u"你有一条新的通知公告：%s" % target.title, *[user.registration_id for user in target.authorized_users])


@listens_for(Bulletin.status, "set")
def push_after_status_set(target, value, oldvalue, initiator):
    if not oldvalue and value:
        push(u"你有一条新的通知公告：%s" % target.title, *[user.registration_id for user in target.authorized_users])
