# -*- coding: utf-8 -*-

"""

    zhifang.app.api.reimbursement
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/04/17

"""


import traceback

from flask import abort, current_app, jsonify, request

from flask_security import auth_token_required, current_user


from app.models.reimbursement import Reimbursement
from app.models.audit_view import AuditView
from app.models.project import Project
from app.models.user import User
from app.models import db

from . import api


@api.route("/reimbursement", methods=["POST"])
@auth_token_required
def create_reimbursement():

    try:

        request_json = request.get_json(force=1)

        reimbursement_type_id = request_json.get("reimbursement_type_id")

        project_id = request_json.get("project_id")

        attachment = request_json.get("attachment")

        notation = request_json.get("notation")

        amount = request_json.get("amount")

        if reimbursement_type_id and project_id and amount:

            reimbursement = Reimbursement(reimbursement_type_id=reimbursement_type_id,
                                          create_user_id=current_user.id,
                                          project_id=project_id,
                                          attachment=attachment,
                                          notation=notation,
                                          amount=amount)

            reimbursement.save()

            rd3_audit_view = AuditView(audit_user=User.query.filter_by(username=u"杨好三").first(),
                                       audit_item=reimbursement)

            rd3_audit_view.save()

            nd2_audit_view = AuditView(audit_user=current_user.region.charge_user, audit_item=reimbursement,
                                       next_id=rd3_audit_view.id)

            nd2_audit_view.save()

            st1_audit_view = AuditView(audit_user=Project.query.get(project_id).charge_user, audit_item=reimbursement,
                                       next_id=nd2_audit_view.id, status=1)

            st1_audit_view.save()

            reimbursement.current_audit_view = st1_audit_view

            db.session.commit()

            data_dict = dict(reimbursement_id=reimbursement.id)

            return jsonify(data_dict)

        else:

            return "Bad Request", 400

    except:

        db.session.rollback()

        current_app.logger.error(traceback.format_exc())

        abort(500, traceback.format_exc())
