# -*- coding: utf-8 -*-

"""

    zhifang.app.api.audit_item
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/25/17

"""


import traceback

from flask import abort, current_app, jsonify, request

from flask_security import auth_token_required, current_user

from app.models.audit_item import AuditItem

from . import api


def to_dict(item):

    item_dict = item.to_dict(2, include=["reimbursement_type", "project_stage",
                                         "create_user", "leave_type",
                                         "specialty", "work_type",
                                         "project"])

    item_dict["current_audit_view"] = item.current_audit_view.to_dict(3, include=["last", "audit_user"])

    return item_dict


@api.route("/audit_item")
@auth_token_required
def select_audit_item():

    try:

        used = request.args.get("used")

        type = request.args.getlist("type")

        page = request.args.get("page", default=1, type=int)

        page_size = request.args.get("page_size", default=5, type=int)

        if used == "select":

            audit_items = AuditItem.query.filter(AuditItem.create_user == current_user)

            if type:

                audit_items = audit_items.filter(AuditItem.type.in_(type))

        if used == "update":

            audit_items = AuditItem.query.filter(AuditItem.current_audit_view.audit_user == current_user)

        audit_items = audit_items.order_by(AuditItem.create_datetime.desc()).paginate(page, page_size)

        data_dict = dict()

        data_dict["audit_items"] = [to_dict(item) for item in audit_items]

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
