# -*- coding: utf-8 -*-

"""

    zhifang.app.admin.role
    ~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/26/17

"""


from . import AppModelView


class RoleModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    labels = dict(name=u"权限", description=u"描述", users=u"用户")

    column_labels = labels
