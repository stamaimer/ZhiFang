# -*- coding: utf-8 -*-

"""

    zhifang.app.api.work
    ~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/04/17

"""


import traceback

from flask import abort, current_app, jsonify, request

from flask_security import auth_token_required, current_user

from app.models.audit_view import AuditView
from app.models.project import Project
from app.models.work import Work
from app.models import db

from . import api


@api.route("/work", methods=["POST"])
@auth_token_required
def create_work():

    try:

        request_json = request.get_json(force=1)

        project_stage_id = request_json.get("project_stage_id")

        specialty_id = request_json.get("specialty_id")

        work_type_id = request_json.get("work_type_id")

        project_id = request_json.get("project_id")

        notation = request_json.get("notation")

        date = request_json.get("date")

        hour = request_json.get("hour")

        if project_stage_id and specialty_id and work_type_id and project_id and date and hour:

            work = Work(project_stage_id=project_stage_id,
                        create_user_id=current_user.id,
                        specialty_id=specialty_id,
                        work_type_id=work_type_id,
                        project_id=project_id,
                        notation=notation,
                        date=date,
                        hour=hour)

            work.save()

            st1_audit_view = AuditView(audit_user=Project.query.get(project_id).charge_user,
                                       audit_item=work, status=1)

            st1_audit_view.save()

            work.current_audit_view = st1_audit_view

            db.session.commit()

            data_dict = dict(work_id=work.id)

            return jsonify(data_dict)

        else:

            return "Bad Request", 400

    except:

        db.session.rollback()

        current_app.logger.error(traceback.format_exc())

        abort(500, traceback.format_exc())
