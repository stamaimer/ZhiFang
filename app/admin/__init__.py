# -*- coding: utf-8 -*-

"""

    zhifang.app.admin
    ~~~~~~~~~~~~~~~~~

    stamaimer 02/22/17

"""


from flask import redirect, request, url_for

from flask_security import current_user

from flask_admin import Admin
from flask_admin.contrib import fileadmin
from flask_admin.contrib.sqla import ModelView

from app.models import db
from app.models.role import Role
from app.models.user import User
from app.models.loan import Loan
from app.models.work import Work
from app.models.clock import Clock
from app.models.leave import Leave
from app.models.region import Region
from app.models.project import Project
from app.models.bulletin import Bulletin
from app.models.work_type import WorkType
from app.models.specialty import Specialty
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

    # pass


class RegionModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    form_columns = ["text", "charge_user", "status"]

    labels = dict(text=u"地域", charge_user=u"负责人员", status=u"状态")

    column_labels = labels


class WorkTypeModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    labels = dict(text=u"工作类型", status=u"状态")

    column_labels = labels


class SpecialtyModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    labels = dict(text=u"专业类型", status=u"状态")

    column_labels = labels


class LeaveTypeModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    labels = dict(text=u"请假类型", status=u"状态")

    column_labels = labels


class ProjectStageModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    labels = dict(text=u"项目节点", status=u"状态")

    column_labels = labels


class ReimbursementTypeModelView(AppModelView):

    column_exclude_list = ["create_datetime", "update_datetime"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    labels = dict(text=u"报销类型", status=u"状态")

    column_labels = labels


admin = Admin(name=u"智方后台管理", template_mode="bootstrap3")

from .reimbursement import ReimbursementModelView
from .bulletin import BulletinModelView
from .project import ProjectModelView
from .clock import ClockModelView
from .leave import LeaveModelView
from .loan import LoanModelView
from .user import UserModelView
from .role import RoleModelView
from .work import WorkModelView


admin.add_view(BulletinModelView(Bulletin, db.session, name=u"公告"))
admin.add_view(ProjectModelView(Project, db.session, name=u"项目"))
admin.add_view(UserModelView(User, db.session, name=u"用户"))
admin.add_view(ClockModelView(Clock, db.session, name=u"打卡"))
admin.add_view(LeaveModelView(Leave, db.session, name=u"请假"))
admin.add_view(WorkModelView(Work, db.session, name=u"工时"))
admin.add_view(LoanModelView(Loan, db.session, name=u"借款"))
admin.add_view(ReimbursementModelView(Reimbursement, db.session, name=u"报销"))
admin.add_view(RoleModelView(Role, db.session, name=u"权限", category=u"辅助数据"))
admin.add_view(RegionModelView(Region, db.session, name=u"地域", category=u"辅助数据"))
admin.add_view(WorkTypeModelView(WorkType, db.session, name=u"工作类型", category=u"辅助数据"))
admin.add_view(SpecialtyModelView(Specialty, db.session, name=u"专业类型", category=u"辅助数据"))
admin.add_view(LeaveTypeModelView(LeaveType, db.session, name=u"请假类型", category=u"辅助数据"))
admin.add_view(ProjectStageModelView(ProjectStage, db.session, name=u"项目节点", category=u"辅助数据"))
admin.add_view(ReimbursementTypeModelView(ReimbursementType, db.session, name=u"报销类型", category=u"辅助数据"))
admin.add_view(fileadmin.FileAdmin("app/static/apk", "/static/apk/", name="Android"))
