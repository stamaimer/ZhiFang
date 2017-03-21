# -*- coding: utf -*-

"""

    zhifang.app.form
    ~~~~~~~~~~~~~~~~

    stamaimer 03/21/17

"""


from wtforms.fields import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from flask_security.forms import LoginForm


class AppLoginForm(LoginForm):

    email = StringField(u"账户", [DataRequired()])

    password = PasswordField(u"密码", [DataRequired()])

    remember = BooleanField(u"记住我")

    submit = SubmitField(u"登录")
