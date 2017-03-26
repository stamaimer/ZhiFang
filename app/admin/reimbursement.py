# -*- coding: utf-8 -*-

"""

    zhifang.app.admin.reimbursement
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/26/17

"""


from jinja2 import Markup

from ..models.audit_view import AuditView

from . import AppModelView


class ReimbursementModelView(AppModelView):

    can_edit = 0

    can_create = 0

    can_delete = 0

    can_view_details = 1

    def _list_thumbnail(view, context, model, name):

        if not model.attachment:

            return ''

        return Markup('<img src="{}" style="width:100%">'.format(model.attachment))

    def _list_audit_process(view, context, model, name):

        audit_views = AuditView.query.filter_by(audit_item_id=model.id, status=1)\
            .order_by(AuditView.update_datetime).all()

        return Markup("<br />".join(["<pre>" + item.__repr__() + "</pre>" for item in audit_views]))

    column_formatters = {
        "attachment": _list_thumbnail,
        "audit_process": _list_audit_process
    }

    column_default_sort = ("create_datetime", 1)

    column_list = ["create_user", "amount", "project", "reimbursement_type", "notation", "create_datetime", "status"]

    column_details_list = ["create_user", "amount", "project", "reimbursement_type", "notation", "create_datetime",
                           "status", "attachment", "audit_process"]

    column_searchable_list = ["create_user.username", "project.name", "reimbursement_type.text", "status"]

    labels = dict(create_user=u"创建人员", amount=u"金额", project=u"所属项目", reimbursement_type=u"报销类型",
                  notation=u"备注", create_datetime=u"创建时间", status=u"状态", attachment=u"附件", audit_process=u"审批流程")

    column_labels = labels
