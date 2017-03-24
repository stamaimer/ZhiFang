# -*- coding: utf-8 -*-

"""

    zhifang.app.api.leave
    ~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/01/17

"""


import traceback

from flask import abort, current_app, jsonify, request

from flask_security import auth_token_required, current_user

from app.models.audit_view import AuditView
from app.models.audit import Audit
from app.models.leave import Leave
from app.models.user import User

from app.utilities import push

from . import api


@api.route("/leave", methods=["POST"])
@auth_token_required
def create_leave():

    try:

        request_json = request.get_json(force=1)

        leave_type_id = request_json.get("leave_type_id")

        beg_date = request_json.get("beg_date")

        end_date = request_json.get("end_date")

        notation = request_json.get("notation")

        last = request_json.get("last")

        audit = Audit(create_user=current_user, type=u"请假")

        audit.save()

        rd3_audit_view = AuditView(audit_user=User.query.get(1), audit=audit)  #

        rd3_audit_view.save()

        nd2_audit_view = AuditView(audit_user=current_user.region.charge_user, audit=audit,
                                   next_id=rd3_audit_view.id, status=1)

        nd2_audit_view.save()

        audit.current = nd2_audit_view

        leave = Leave(create_user_id=current_user.id,
                      leave_type_id=leave_type_id,
                      audit_id=audit.id,
                      beg_date=beg_date,
                      end_date=end_date,
                      notation=notation,
                      last=last)

        leave.save()

        push(u"你有一条来自{}的{}申请".format(current_user.username, audit.type),
             nd2_audit_view.audit_user.registration_id)  #

        data_dict = dict(leave_id=leave.id)

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
