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


class AppModelView(ModelView):

    """

        Add  Authorization & Permissions

        https://flask-admin.readthedocs.io/en/latest/introduction/#authorization-permissions

    """

    def is_accessible(self):

        return current_user.has_role("admin")

    def inaccessible_callback(self, name, **kwargs):

        return redirect(url_for("security.login", next=request.url))


admin = Admin(name="Dashboard", template_mode="bootstrap3")

admin.add_view(AppModelView(Role, db.session))
admin.add_view(AppModelView(User, db.session))
