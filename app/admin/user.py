# -*- coding: utf-8 -*-

"""

    zhifang.app.admin.user
    ~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/26/17

"""


import time
import hashlib

from jinja2 import Markup

from flask import url_for

from flask_admin import form

from . import AppModelView


class UserModelView(AppModelView):

    can_view_details = 1

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

    def get_query(self):

        return self.session.query(self.model).filter(self.model.roles.any(name="general"))

    def get_count_query(self):

        return self.get_query().count()

    form_excluded_columns = ["create_datetime", "update_datetime", "email", "registration_id"]

    column_searchable_list = ["employee_no", "username", "gender", "phone", "id_no", "specialties.text", "region.text",
                              "roles.name", "active", "notation"]

    column_list = ["employee_no", "username", "gender", "phone", "specialties", "region", "roles", "active"]

    column_details_list = ["employee_no", "username", "gender", "phone", "id_no", "specialties", "region", "roles",
                           "active", "image", "notation", "create_datetime", "update_datetime"]

    form_columns = ["employee_no", "username", "password", "gender", "phone", "id_no", "specialties", "region", "roles",
                    "active", "notation", "image"]

    labels = dict(employee_no=u"工号", username=u"姓名", password=u"密码", gender=u"性别", phone=u"手机", id_no=u"身份证号",
                  specialties=u"专业", region=u"地域", roles=u"权限", active=u"状态", image=u"签名", notation=u"备注",
                  create_datetime=u"创建时间", update_datetime=u"修改时间")

    column_labels = labels
