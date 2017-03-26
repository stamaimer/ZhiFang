# -*- coding: utf-8 -*-

"""

    zhifang.app.api.project
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 02/28/17

"""


import traceback

from flask import abort, current_app, jsonify

from flask_security import auth_token_required

from app.models.project import Project

from . import api


@api.route("/project")
@auth_token_required
def select_project():

    try:

        projects = Project.query.filter_by(status=1).order_by(Project.create_datetime.desc()).all()

        data_dict = dict(projects=[project.to_dict() for project in projects])

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
