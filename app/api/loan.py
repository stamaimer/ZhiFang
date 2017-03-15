# -*- coding: utf-8 -*-

"""

    zhifang.app.api.loan
    ~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/04/17

"""


import traceback

from flask import abort, current_app, jsonify, request

from flask_security import auth_token_required, current_user

from app.models.audit_view import AuditView
from app.models.project import Project
from app.models.audit import Audit
from app.models.loan import Loan
from app.models.user import User
from app.models import db

from app.utilities import push

from . import api


@api.route("/loan", methods=["POST"])
@auth_token_required
def create_loan():

    try:

        request_json = request.get_json(force=1)

        project_id = request_json["project_id"]

        attachment = request_json["attachment"]

        notation = request_json["notation"]

        amount = request_json["amount"]

        audit = Audit(create_user=current_user, type=u"借款")

        audit.save()

        rd3_audit_view = AuditView(audit_user=User.query.get(1), audit=audit)

        rd3_audit_view.save()

        nd2_audit_view = AuditView(audit_user=current_user.region.charge_user, audit=audit)

        nd2_audit_view.save()

        nd2_audit_view._next_ = rd3_audit_view

        st1_audit_view = AuditView(audit_user=Project.query.get(project_id).charge_user, audit=audit, status=1)

        st1_audit_view.__next__ = nd2_audit_view

        st1_audit_view.save()

        audit.current = st1_audit_view

        loan = Loan(create_user_id=current_user.id,
                    project_id=project_id,
                    attachment=attachment,
                    audit_id=audit.id,
                    notation=notation,
                    amount=amount)

        loan.save()

        push(u"你有一条来自{}的{}申请".format(current_user.username, audit.type),
             st1_audit_view.audit_user.registration_id)

        data_dict = dict(loan=loan.to_dict())

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
