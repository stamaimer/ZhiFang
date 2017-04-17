# -*- coding: utf-8 -*-

"""

    zhifang.app.admin.loan
    ~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/26/17

"""


from jinja2 import Markup

from flask import redirect, request, url_for

from flask_security import current_user

from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import EndpointLinkRowAction

from ..models.audit_view import AuditView


class LoanModelView(ModelView):

    def is_accessible(self):

        return current_user.has_role("admin") or current_user.has_role("test") or current_user.has_role("cashier")

    def inaccessible_callback(self, name, **kwargs):

        return redirect(url_for("security.login", next=request.url))

    can_export = 1

    can_set_page_size = 1

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

    column_extra_row_actions = [
        EndpointLinkRowAction("glyphicon glyphicon-file", "main.generate_loan_certificate")
    ]

    column_default_sort = ("create_datetime", 1)

    column_list = ["create_user", "amount", "project", "create_datetime", "status", "printed"]

    column_details_list = ["create_user", "amount", "project", "notation", "create_datetime", "status", "printed",
                           "audit_process", "attachment"]

    column_editable_list = ["printed"]

    column_searchable_list = ["create_user.username", "project.name", "status", "printed"]

    labels = dict(create_user=u"创建人员", amount=u"金额", project=u"所属项目", notation=u"备注",
                  create_datetime=u"创建时间", status=u"状态", printed=u"打印与否", attachment=u"附件",
                  audit_process=u"审批流程")

    column_labels = labels
