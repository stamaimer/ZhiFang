# -*- coding: utf-8 -*-

"""

    zhifang.app.admin.bulletin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/26/17

"""


import os
import ast
import time
import hashlib

from PIL import Image

from jinja2 import Markup

from wtforms import TextAreaField, ValidationError
from wtforms.utils import unset_value
from wtforms.widgets import html_params, HTMLString, TextArea

from flask import url_for

from flask_admin import form
from flask_admin.helpers import get_url
from flask_admin._compat import string_types, urljoin
from flask_admin.form.upload import ImageUploadField

from . import AppModelView


class CKTextAreaWidget(TextArea):

    def __call__(self, field, **kwargs):

        if kwargs.get('class'):

            kwargs['class'] += ' ckeditor'

        else:

            kwargs.setdefault('class', 'ckeditor')

        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):

    widget = CKTextAreaWidget()


class MultipleImageUploadInput(object):

    empty_template = "<input %(file)s multiple>"

    data_template = ("<div class='image-thumbnail'>"
                     "  %(images)s"
                     "</div>"
                     "<input %(file)s multiple>")

    def __call__(self, field, **kwargs):

        kwargs.setdefault("id", field.id)
        kwargs.setdefault("name", field.name)

        args = {"file": html_params(type="file", **kwargs)}

        if field.data and isinstance(field.data, string_types):

            attributes = self.get_attributes(field)

            args["images"] = "&emsp;".join([u"<img src='{}' /><input type='checkbox' name='_{}-delete'>删除</input>"
                                            .format(src, filename) for src, filename in attributes])

            template = self.data_template

        else:
            template = self.empty_template

        return HTMLString(template % args)

    def get_attributes(self, field):

        for item in ast.literal_eval(field.data):

            filename = item

            if field.thumbnail_size:

                filename = field.thumbnail_fn(filename)

            if field.url_relative_path:

                filename = urljoin(field.url_relative_path, filename)

            yield get_url(field.endpoint, filename=filename), item


class MultipleImageUploadField(ImageUploadField):

    widget = MultipleImageUploadInput()

    def process(self, formdata, data=unset_value):

        self.formdata = formdata

        return super(MultipleImageUploadField, self).process(formdata, data)

    def process_formdata(self, valuelist):

        self.data = list()

        for value in valuelist:

            if self._is_uploaded_file(value):

                self.data.append(value)

    def populate_obj(self, obj, name):

        field = getattr(obj, name, None)

        if field:

            filenames = ast.literal_eval(field)

            for filename in filenames[:]:

                if "_{}-delete".format(filename) in self.formdata:

                    self._delete_file(filename)

                    filenames.remove(filename)

        else:

            filenames = list()

        for data in self.data:

            if self._is_uploaded_file(data):

                try:

                    self.image = Image.open(data)

                except Exception as e:

                    raise ValidationError('Invalid image: %s' % e)

                filename = self.generate_name(obj, data)

                filename = self._save_file(data, filename)

                data.filename = filename

                filenames.append(filename)

        setattr(obj, name, str(filenames))


class BulletinModelView(AppModelView):

    can_view_details = 1

    edit_template = "admin/edit.html"

    create_template = "admin/create.html"

    form_overrides = {"content": CKTextAreaField}

    def _show_html_code(view, context, model, name):

        if not model.content:

            return ''

        return Markup(model.content)

    def _list_thumbnail(view, context, model, name):

        if not model.image:

            return ''

        def gen_img(filename):

            return '<img src="{}">'.format(url_for('static', filename="images/bulletin/"
                                                                      + form.thumbgen_filename(filename)))

        return Markup("<br />".join([gen_img(image) for image in ast.literal_eval(model.image)]))

    column_formatters = {'image': _list_thumbnail, 'content': _show_html_code}

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.

    def namegen(obj, image):

        filename = hashlib.md5(os.urandom(47) + str(time.time())).hexdigest()[:9]

        return filename

    form_extra_fields = {
        'image': MultipleImageUploadField(u"附件",
                                      base_path="app/static/images/bulletin",
                                      url_relative_path="images/bulletin/",
                                      thumbnail_size=(400, 300, 1),
                                      namegen=namegen)
    }

    column_list = ["create_datetime", "title"]

    column_default_sort = ("create_datetime", 1)

    column_details_list = ["title", "content", "authorized_users", "status", "create_datetime", "update_datetime", "image"]

    form_excluded_columns = ["create_datetime", "update_datetime"]

    column_searchable_list = ["title", "content", "authorized_users.username", "status"]

    form_columns = ["title", "content", "authorized_users", "status", "image"]

    labels = dict(title=u"标题", content=u"内容", authorized_users=u"授权用户", status=u"状态", image=u"附件",
                  create_datetime=u"创建时间", update_datetime=u"修改时间")

    column_labels = labels
