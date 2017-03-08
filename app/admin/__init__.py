# -*- coding: utf-8 -*-

"""

    zhifang.app.admin
    ~~~~~~~~~~~~~~~~~

    stamaimer 02/22/17

"""


from flask import redirect, request, url_for

from flask_security import current_user

from flask_admin import Admin
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

    # def is_accessible(self):
    #
    #     return current_user.has_role("admin")
    #
    # def inaccessible_callback(self, name, **kwargs):
    #
    #     return redirect(url_for("security.login", next=request.url))


class RoleModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    labels = dict(name=u"权限", description=u"描述")

    column_labels = labels


class UserModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime", "email", "password", "registration_id"]

    labels = dict(region=u"地域", employee_no=u"工号", id_no=u"身份证号", phone=u"手机", active=u"状态", gender=u"性别",
                  username=u"姓名")

    column_labels = labels


class LoanModelView(AppModelView):

    column_exclude_list = ["update_datetime", "audit_item_type"]

    labels = dict(project=u"所属项目", create_user=u"创建人", create_datetime=u"创建时间", attachment=u"附件",
                  amount=u"金额", notation=u"备注", audit=u"状态")

    column_labels = labels


class WorkModelView(AppModelView):

    column_exclude_list = ["update_datetime", "audit_item_type"]

    labels = dict(project=u"所属项目", project_stage=u"所属项目节点", specialty=u"专业", work_type=u"工作内容",
                  create_user=u"创建人", create_datetime=u"创建时间", attachment=u"附件", date=u"所属日期", hour=u"工时",
                  notation=u"备注", audit=u"状态")

    column_labels = labels


class AuditModelView(AppModelView):

    column_exclude_list = ["update_datetime"]

    labels = dict(current=u"待审", create_user=u"创建人", create_datetime=u"创建时间", status=u"状态", type=u"类型")

    column_labels = labels


class ClockModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    labels = dict(project=u"所属项目", user=u"打卡人", notation=u"备注", position=u"打卡位置", datetime=u"打卡时间")

    column_labels = labels


class LeaveModelView(AppModelView):

    column_exclude_list = ["update_datetime", "audit_item_type"]

    labels = dict(leave_type=u"请假类型", create_user=u"创建人", create_datetime=u"创建时间", attachment=u"附件",
                  notation=u"备注", beg_date=u"开始日期", end_date=u"结束日期", last=u"持续天数", audit=u"状态")

    column_labels = labels


class RegionModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    labels = dict(charge_user=u"负责人", text=u"地域")

    column_labels = labels


class ProjectModelView(AppModelView):

    column_exclude_list = ["update_datetime"]

    labels = dict(region=u"所属地域", charge_user=u"负责人", current_stage=u"当前节点", create_datetime=u"创建时间",
                  no=u"项目编号", name=u"项目名称")

    column_labels = labels


class BulletinModelView(AppModelView):

    column_exclude_list = ["update_datetime"]

    labels = dict(create_datetime=u"创建时间", title=u"标题", content=u"内容")

    column_labels = labels


class WorkTypeModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    labels = dict(text=u"工作类型")

    column_labels = labels


class SpecialtyModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    labels = dict(text=u"专业类型")

    column_labels = labels


class AuditItemModelView(AppModelView):

    column_exclude_list = ["update_datetime"]

    labels = dict(create_user=u"创建人", create_datetime=u"创建时间", attachment=u"附件", audit_item_type=u"类型",
                  audit=u"状态")

    column_labels = labels


class AuditViewModelView(AppModelView):

    column_exclude_list = ["_next_", "update_datetime"]

    labels = dict(audit_user=u"审批人", create_datetime=u"创建时间", advice=u"意见", status=u"状态", result=u"结果",
                  audit=u"审批状态")

    column_labels = labels


class LeaveTypeModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    labels = dict(text=u"请假类型")

    column_labels = labels


class ProjectStageModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    labels = dict(text=u"项目节点")

    column_labels = labels


class ReimbursementModelView(AppModelView):

    column_exclude_list = ["update_datetime", "audit_item_type"]

    labels = dict(project=u"所属项目", reimbursement_type=u"报销类型", create_user=u"创建人", create_datetime=u"创建时间",
                  attachment=u"附件", amount=u"金额", notation=u"备注", audit=u"状态")

    column_labels = labels


class ReimbursementTypeModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

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
admin.add_view(AuditItemModelView(AuditItem, db.session, name=u"审批项目"))
admin.add_view(AuditViewModelView(AuditView, db.session, name=u"审批条目"))
admin.add_view(AuditModelView(Audit, db.session, name=u"审批"))
admin.add_view(RoleModelView(Role, db.session, name=u"权限", category=u"辅助数据"))
admin.add_view(RegionModelView(Region, db.session, name=u"地域", category=u"辅助数据"))
admin.add_view(WorkTypeModelView(WorkType, db.session, name=u"工作类型", category=u"辅助数据"))
admin.add_view(SpecialtyModelView(Specialty, db.session, name=u"专业类型", category=u"辅助数据"))
admin.add_view(LeaveTypeModelView(LeaveType, db.session, name=u"请假类型", category=u"辅助数据"))
admin.add_view(ProjectStageModelView(ProjectStage, db.session, name=u"项目节点", category=u"辅助数据"))
admin.add_view(ReimbursementTypeModelView(ReimbursementType, db.session, name=u"报销类型", category=u"辅助数据"))
