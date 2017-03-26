# -*- coding: utf-8 -*-

"""

    zhifang.app.admin.leave
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/16/17

"""


from jinja2 import Markup

from ..models.audit_view import AuditView

from . import AppModelView


class LeaveModelView(AppModelView):

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

    column_list = ["create_user", "leave_type", "beg_date", "end_date", "last", "notation", "create_datetime", "status"]

    column_details_list = ["create_user", "leave_type", "beg_date", "end_date", "last", "notation", "create_datetime",
                           "status", "audit_process"]

    column_searchable_list = ["create_user.username", "leave_type.text", "status"]

    labels = dict(create_user=u"创建人员", leave_type=u"请假类型", beg_date=u"开始日期", end_date=u"结束日期", last=u"持续天数",
                  notation=u"备注", create_datetime=u"创建时间", status=u"状态", audit_process=u"审批流程")

    column_labels = labels
