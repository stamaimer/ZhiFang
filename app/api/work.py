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
from app.models.audit import Audit
from app.models.work import Work

from app.utilities import push

from . import api


@api.route("/work", methods=["POST"])
@auth_token_required
def create_work():

    try:

        request_json = request.get_json(force=1)

        project_stage_id = request_json["project_stage_id"]

        specialty_id = request_json["specialty_id"]

        work_type_id = request_json["work_type_id"]

        project_id = request_json["project_id"]

        notation = request_json["notation"]

        hour = request_json["hour"]

        date = request_json["date"]

        audit = Audit(create_user=current_user, type=u"工时")

        audit.save()

        st1_audit_view = AuditView(audit_user=Project.query.get(project_id).charge_user, audit=audit, status=1)

        st1_audit_view.save()

        audit.current = st1_audit_view

        work = Work(project_stage_id=project_stage_id,
                    create_user_id=current_user.id,
                    specialty_id=specialty_id,
                    work_type_id=work_type_id,
                    project_id=project_id,
                    audit_id=audit.id,
                    notation=notation,
                    date=date,
                    hour=hour)

        work.save()

        push(u"你有一条来自{}的{}申请".format(current_user.username, audit.type),
             st1_audit_view.audit_user.registration_id)

        data_dict = dict(work=work.to_dict())

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)





