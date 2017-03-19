# -*- coding: utf-8 -*-

"""

    zhifang.app.admin
    ~~~~~~~~~~~~~~~~~

    stamaimer 02/22/17

"""


import time
import hashlib

from jinja2 import Markup

from flask import redirect, request, url_for

from flask_security import current_user

from flask_admin import Admin, form
from flask_admin.contrib.sqla import ModelView

from app.models import db
from app.models.role import Role
from app.models.user import User
from app.models.loan import Loan
from app.models.work import Work
from app.models.audit import Audit
from app.models.clock import Clock
from app.models.leave import Leave
from app.models.region import Region
from app.models.project import Project
from app.models.bulletin import Bulletin
from app.models.work_type import WorkType
from app.models.specialty import Specialty
from app.models.audit_item import AuditItem
from app.models.audit_view import AuditView
from app.models.leave_type import LeaveType
from app.models.project_stage import ProjectStage
from app.models.reimbursement import Reimbursement
from app.models.reimbursement_type import ReimbursementType


class AppModelView(ModelView):

    """

        Add  Authorization & Permissions

        https://flask-admin.readthedocs.io/en/latest/introduction/#authorization-permissions

    """

    def is_accessible(self):

        return current_user.has_role("admin")

    def inaccessible_callback(self, name, **kwargs):

        return redirect(url_for("security.login", next=request.url))


class RoleModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    labels = dict(name=u"权限", description=u"描述", users=u"用户")

    column_labels = labels


class UserModelView(AppModelView):

    can_view_details = True

    def _list_thumbnail(view, context, model, name):

        if not model.image:

            return ''

        return Markup('<img src="{}" style="width:100px">'.format(url_for('static',
                                                                          filename="images/sign/" + model.image)))

    column_formatters = {
        'image': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.

    def namegen(obj, image):

        return hashlib.md5(str(time.time())).hexdigest()[:28]

    form_extra_fields = {
        'image': form.ImageUploadField(u'签名',
                                      base_path="app/static/images/sign",
                                      url_relative_path="images/sign/",
                                      namegen=namegen)
    }

    column_exclude_list = ["create_datetime", "update_datetime", "email", "image", "password", "registration_id"]

    form_excluded_columns = ["create_datetime", "update_datetime", "email", "registration_id", "clocks"]

    column_details_exclude_list = ["email", "registration_id"]

    column_searchable_list = ["region.text", "username"]

    labels = dict(region=u"地域", roles=u"权限", specialties=u"专业", employee_no=u"工号", id_no=u"身份证号", phone=u"手机",
                  image=u"签名", active=u"状态", gender=u"性别", username=u"姓名", password=u"密码", notation=u"备注",
                  create_datetime=u"创建时间", update_datetime=u"修改时间")

    column_labels = labels


class LoanModelView(AppModelView):

    can_edit = False

    can_create = False

    can_delete = False

    can_view_details = True

    def _list_thumbnail(view, context, model, name):

        if not model.attachment:

            return ''

        return Markup('<img src="{}" style="width:100%">'.format(model.attachment))

    column_formatters = {
        "attachment": _list_thumbnail
    }

    column_exclude_list = ["attachment", "update_datetime", "audit_item_type"]

    column_details_exclude_list = ["update_datetime", "audit_item_type"]

    labels = dict(project=u"所属项目", create_user=u"创建人", create_datetime=u"创建时间", attachment=u"附件",
                  amount=u"金额", notation=u"备注", audit=u"状态")

    column_labels = labels


class WorkModelView(AppModelView):

    can_edit = False

    can_create = False

    can_delete = False

    can_view_details = True

    column_exclude_list = ["attachment", "update_datetime", "audit_item_type"]

    column_details_exclude_list = column_exclude_list

    labels = dict(project=u"所属项目", project_stage=u"所属项目节点", specialty=u"专业", work_type=u"工作内容",
                  create_user=u"创建人", create_datetime=u"创建时间", attachment=u"附件", date=u"所属日期", hour=u"工时",
                  notation=u"备注", audit=u"状态")

    column_labels = labels


class AuditModelView(AppModelView):

    can_edit = False

    can_create = False

    can_delete = False

    can_view_details = True

    # column_exclude_list = ["update_datetime"]

    def _current_formatter(view, context, model, name):

        if model.status == u"审批中":

            return model.current.audit_user.username

        else:

            return ""

    def _audit_views_formatter(view, context, model, name):

        return Markup("<br />".join(["<pre>" + item.__repr__() + "</pre>" for item in model.audit_views if item.status == 1]))

    def _audit_items_formatter(view, context, model, name):

        if model.audit_items[0].audit_item_type == u"请假":

            return Markup(u"<a href='{}'>{}</a>".format(url_for("leave.details_view",
                                                                id=model.audit_items[0].id),
                                                                model.type))

        if model.audit_items[0].audit_item_type == u"工时":

            return Markup(u"<a href='{}'>{}</a>".format(url_for("work.details_view",
                                                                id=model.audit_items[0].id),
                                                                model.type))

        if model.audit_items[0].audit_item_type == u"借款":

            return Markup(u"<a href='{}'>{}</a>".format(url_for("loan.details_view",
                                                                id=model.audit_items[0].id),
                                                                model.type))

        if model.audit_items[0].audit_item_type == u"报销":

            return Markup(u"<a href='{}'>{}</a>".format(url_for("reimbursement.details_view",
                                                                id=model.audit_items[0].id),
                                                                model.type))

    column_formatters = {
        "current": _current_formatter,
        "audit_views": _audit_views_formatter,
        "audit_items": _audit_items_formatter
    }

    column_list = ["current", "create_user", "create_datetime", "status", "audit_items", "audit_views"]

    labels = dict(current=u"待审", create_user=u"创建人", create_datetime=u"创建时间", status=u"状态", type=u"类型",
                  audit_items=u"详情", audit_views=u"审批流程")

    column_labels = labels


class ClockModelView(AppModelView):

    can_edit = False

    can_create = False

    can_delete = False

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    column_searchable_list = ["project.name", "user.username"]

    labels = dict(project=u"所属项目", user=u"打卡人", notation=u"备注", position=u"打卡位置", datetime=u"打卡时间")

    column_labels = labels


class LeaveModelView(AppModelView):

    can_edit = False

    can_create = False

    can_delete = False

    can_view_details = True

    column_exclude_list = ["attachment", "update_datetime", "audit_item_type"]

    column_details_exclude_list = column_exclude_list

    column_searchable_list = ["create_user.username"]

    labels = dict(leave_type=u"请假类型", create_user=u"创建人", create_datetime=u"创建时间", attachment=u"附件",
                  notation=u"备注", beg_date=u"开始日期", end_date=u"结束日期", last=u"持续天数", audit=u"状态")

    column_labels = labels


class RegionModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime", "projects"]

    labels = dict(charge_user=u"负责人", text=u"地域")

    column_labels = labels


class ProjectModelView(AppModelView):

    can_view_details = True

    column_exclude_list = ["update_datetime"]

    form_excluded_columns = ["update_datetime"]

    labels = dict(region=u"所属地域", charge_user=u"负责人", current_stage=u"当前节点", create_datetime=u"创建时间",
                  update_datetime=u"修改时间", no=u"项目编号", name=u"项目名称")

    column_labels = labels


class BulletinModelView(AppModelView):

    can_view_details = True

    column_exclude_list = ["update_datetime", "content"]

    form_excluded_columns = ["update_datetime"]

    labels = dict(create_datetime=u"创建时间", update_datetime=u"修改时间", title=u"标题", content=u"内容")

    column_labels = labels


class WorkTypeModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    labels = dict(text=u"工作类型")

    column_labels = labels


class SpecialtyModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime", "users"]

    labels = dict(text=u"专业类型")

    column_labels = labels


class AuditItemModelView(AppModelView):

    can_edit = False

    can_create = False

    can_delete = False

    column_exclude_list = ["attachment", "update_datetime"]

    labels = dict(create_user=u"创建人", create_datetime=u"创建时间", audit_item_type=u"类型", audit=u"状态")

    column_labels = labels


class AuditViewModelView(AppModelView):

    can_edit = False

    can_create = False

    can_delete = False

    column_exclude_list = ["_next_", "update_datetime"]

    labels = dict(audit_user=u"审批人", create_datetime=u"创建时间", advice=u"意见", status=u"状态", result=u"结果",
                  audit=u"审批状态")

    column_labels = labels


class LeaveTypeModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    labels = dict(text=u"请假类型")

    column_labels = labels


class ProjectStageModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    labels = dict(text=u"项目节点")

    column_labels = labels


class ReimbursementModelView(AppModelView):

    can_edit = False

    can_create = False

    can_delete = False

    can_view_details = True

    def _list_thumbnail(view, context, model, name):

        if not model.attachment:

            return ''

        return Markup('<img src="{}" style="width:100%">'.format(model.attachment))

    column_formatters = {
        "attachment": _list_thumbnail
    }

    column_exclude_list = ["attachment", "update_datetime", "audit_item_type"]

    column_details_exclude_list = ["update_datetime", "audit_item_type"]

    labels = dict(project=u"所属项目", reimbursement_type=u"报销类型", create_user=u"创建人", create_datetime=u"创建时间",
                  attachment=u"附件", amount=u"金额", notation=u"备注", audit=u"状态")

    column_labels = labels


class ReimbursementTypeModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    labels = dict(text=u"报销类型")

    column_labels = labels


admin = Admin(name=u"智方后台管理", template_mode="bootstrap3")

admin.add_view(ProjectModelView(Project, db.session, name=u"项目"))
admin.add_view(UserModelView(User, db.session, name=u"用户"))
admin.add_view(ClockModelView(Clock, db.session, name=u"打卡"))
admin.add_view(LeaveModelView(Leave, db.session, name=u"请假"))
admin.add_view(WorkModelView(Work, db.session, name=u"工时"))
admin.add_view(LoanModelView(Loan, db.session, name=u"借款"))
admin.add_view(ReimbursementModelView(Reimbursement, db.session, name=u"报销"))
admin.add_view(BulletinModelView(Bulletin, db.session, name=u"公告"))
# admin.add_view(AuditItemModelView(AuditItem, db.session, name=u"审批项目"))
# admin.add_view(AuditViewModelView(AuditView, db.session, name=u"审批条目"))
admin.add_view(AuditModelView(Audit, db.session, name=u"审批"))
admin.add_view(RoleModelView(Role, db.session, name=u"权限", category=u"辅助数据"))
admin.add_view(RegionModelView(Region, db.session, name=u"地域", category=u"辅助数据"))
admin.add_view(WorkTypeModelView(WorkType, db.session, name=u"工作类型", category=u"辅助数据"))
admin.add_view(SpecialtyModelView(Specialty, db.session, name=u"专业类型", category=u"辅助数据"))
admin.add_view(LeaveTypeModelView(LeaveType, db.session, name=u"请假类型", category=u"辅助数据"))
admin.add_view(ProjectStageModelView(ProjectStage, db.session, name=u"项目节点", category=u"辅助数据"))
admin.add_view(ReimbursementTypeModelView(ReimbursementType, db.session, name=u"报销类型", category=u"辅助数据"))
