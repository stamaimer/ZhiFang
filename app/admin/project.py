# -*- coding: utf-8 -*-

"""

    zhifang.app.admin.project
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/26/17

"""


from . import AppModelView


class ProjectModelView(AppModelView):

    can_view_details = 1

    column_default_sort = ("create_datetime", 1)

    form_excluded_columns = ["create_datetime", "update_datetime"]

    column_searchable_list = ["no", "name", "current_stage.text", "charge_user.username", "region.text", "status"]

    column_list = ["no", "name", "current_stage", "charge_user", "region", "status", "plan_hour", "create_datetime"]

    column_details_list = ["no", "name", "current_stage", "charge_user", "region", "status", "plan_hour",
                           "create_datetime", "update_datetime"]

    form_columns = ["no", "name", "current_stage", "charge_user", "region", "status", "plan_hour"]

    labels = dict(no=u"项目编号", name=u"项目名称", current_stage=u"当前节点", charge_user=u"负责人员", region=u"所属地域",
                  status=u"状态", plan_hour=u"计划工时", create_datetime=u"创建时间", update_datetime=u"修改时间")

    column_labels = labels
