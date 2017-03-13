# -*- coding: utf-8 -*-

"""

    zhifang.app.models.bulletin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/07/17

"""


from sqlalchemy.event import listens_for

from app.utilities import push

from . import db, AppModel


class Bulletin(AppModel):

    title = db.Column(db.String(255))

    content = db.Column(db.Text())


@listens_for(Bulletin, "after_insert")
def push_after_insert(mapper, connection, target):

    push(u"你有一条新的通知公告：%s" % target.title, "all")