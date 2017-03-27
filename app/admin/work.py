# -*- coding: utf-8 -*-

"""

    zhifang.app.admin.work
    ~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/26/17

"""


from jinja2 import Markup

from ..models.audit_view import AuditView

from . import AppModelView


class WorkModelView(AppModelView):

    can_edit = 0

    can_create = 0

    can_delete = 0

    can_view_details = 1

    def _list_audit_process(view, context, model, name):

        audit_views = AuditView.query.filter_by(audit_item_id=model.id, status=1)\
            .order_by(AuditView.update_datetime).all()

        return Markup("<br />".join(["<pre>" + item.__repr__() + "</pre>" for item in audit_views]))

    column_formatters = {
        "audit_process": _list_audit_process
    }

    column_default_sort = ("create_datetime", 1)

    column_list = ["create_user", "specialty", "work_type", "hour", "project", "project_stage", "date", "notation",
                   "create_datetime", "status"]

    column_details_list = ["create_user", "specialty", "work_type", "hour", "project", "project_stage", "date",
                           "notation", "create_datetime", "status", "audit_process"]

    column_searchable_list = ["create_user.username", "specialty.text", "work_type.text", "project.name",
                              "project_stage.text", "status"]

    labels = dict(create_user=u"创建人员", specialty=u"专业", work_type=u"工作内容", hour=u"工时", project=u"所属项目",
                  project_stage=u"所属项目节点", date=u"所属日期", notation=u"备注", create_datetime=u"创建时间",
                  status=u"状态", audit_process=u"审批流程")

    column_labels = labels
