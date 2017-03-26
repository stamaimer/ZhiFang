# -*- coding: utf-8 -*-

"""

    zhifang.app.admin.clock
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/26/17

"""


from . import AppModelView


class ClockModelView(AppModelView):

    can_edit = 0

    can_create = 0

    can_delete = 0

    column_default_sort = ("create_datetime", 1)

    column_list = ["create_user", "datetime", "position", "project", "notation"]

    column_searchable_list = ["create_user.username", "project.name"]

    labels = dict(create_user=u"打卡人员", datetime=u"打卡时间", position=u"打卡位置", project=u"所属项目", notation=u"备注")

    column_labels = labels
