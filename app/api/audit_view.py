# -*- coding: utf-8 -*-

"""

    zhifang.app.api.audit_view
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/04/17

"""


import traceback

from sqlalchemy.sql import func

from flask import abort, current_app, jsonify, request

from flask_security import auth_token_required, current_user

from app.models.audit_view import AuditView
from app.models.user import User
from app.models import db

from app.utilities import push

from . import api


# @api.route("/audit_view")
@auth_token_required
def select_audit_view():

    try:

        audit_views = AuditView.query.filter_by(audit_user_id=current_user.id, status=1, result=None).all()

        data_dict = dict()

        data_dict["audit_views"] = [audit_view.to_dict() for audit_view in audit_views]

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)


@api.route("/audit_view", methods=["PATCH"])
@auth_token_required
def update_audit_view():

    try:

        request_json = request.get_json(force=1)

        audit_view_id = request_json.get("id")

        audit_view = AuditView.query.get(audit_view_id)

        if current_user == audit_view.audit_user:

            result = request_json.get("result")

            advice = request_json.get("advice")

            audit_view.result = result

            audit_view.advice = advice

            audit_view.update_datetime = func.now()

            if result == u"同意":

                if audit_view._next_:

                    audit_view._next_.status = 1

                    audit_view.audit_item.current_audit_view = audit_view._next_

                else:

                    audit_view.audit.status = u"已通过"

            if result == u"驳回":

                audit_view.audit_item.status = u"已驳回"

            if result == u"转审":

                retrial_user_id = request_json.get("retrail_user_id")

                retrial_audit_view = AuditView(audit_user=User.query.get(retrial_user_id),
                                               audit_item=audit_view.audit_item,
                                               status=1)

                retrial_audit_view.save()

                audit_view.audit_item.current_audit_view = retrial_audit_view

                retrial_audit_view._next_ = audit_view._next_

                audit_view._next_ = retrial_audit_view

            db.session.commit()

            return '', 204

        else:

            return '', 401

    except:

        db.session.rollback()

        current_app.logger.error(traceback.format_exc())

        abort(500)
