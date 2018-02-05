# -*- coding: utf-8 -*-

"""

    zhifang.app.api.loan
    ~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/04/17

"""


import traceback

from flask import abort, current_app, jsonify, request

from flask_security import auth_token_required, current_user, login_required

from app.models.audit_view import AuditView
from app.models.project import Project
from app.models.loan import Loan
from app.models.user import User
from app.models import db

from . import api


@api.route("/loan", methods=["POST"])
@auth_token_required
def create_loan():

    try:

        request_json = request.get_json(force=1)

        project_id = request_json.get("project_id")

        attachment = request_json.get("attachment")

        notation = request_json.get("notation")

        amount = request_json.get("amount")

        if project_id and amount:

            loan = Loan(create_user_id=current_user.id,
                        project_id=project_id,
                        attachment=attachment,
                        notation=notation,
                        amount=amount)

            loan.save()

            # th4_audit_view = AuditView(audit_user=User.query.filter_by(username=u"总部出纳").first(), audit_item=loan)
            #
            # th4_audit_view.save()
            #
            # rd3_audit_view = AuditView(audit_user=User.query.filter_by(username=u"杨好三").first(), audit_item=loan,
            #                            next_id=th4_audit_view.id)

            rd3_audit_view = AuditView(audit_user=User.query.filter_by(username=u"杨好三").first(), audit_item=loan)

            rd3_audit_view.save()

            nd2_audit_view = AuditView(audit_user=current_user.region.charge_user, audit_item=loan,
                                       next_id=rd3_audit_view.id)

            nd2_audit_view.save()

            st1_audit_view = AuditView(audit_user=Project.query.get(project_id).charge_user, audit_item=loan,
                                       next_id=nd2_audit_view.id, status=1)

            st1_audit_view.save()

            loan.current_audit_view = st1_audit_view

            db.session.commit()

            data_dict = dict(loan_id=loan.id)

            return jsonify(data_dict)

        else:

            return "Bad Request", 400

    except:

        db.session.rollback()

        current_app.logger.error(traceback.format_exc())

        abort(500, traceback.format_exc())


@api.route("/loan", methods=["PATCH"])
@login_required
def update_loan():

    try:

        request_json = request.get_json(force=1)

        loan_id = request_json.get("loan_id")

        loan = Loan.query.get(loan_id)

        loan.printed = u"已打印"

        db.session.commit()

        return "No Content", 204

    except:

        db.session.rollback()

        current_app.logger.error(traceback.format_exc())

        abort(500, traceback.format_exc())
