# -*- coding: utf-8 -*-

"""

    zhifang.app.api.audit
    ~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/04/17

"""


import traceback

from flask import abort, current_app, jsonify, request

from flask_security import auth_token_required, current_user

from app.models.audit import Audit

from . import api


@api.route("/audit")
@auth_token_required
def select_audit():

    try:

        type = request.args.getlist("type")

        limit = request.args.get("limit")

        if type:

            audits = Audit.query.filter(Audit.create_user == current_user,
                                        Audit.type.op("regexp")('|'.join(type)))\
                .order_by(Audit.create_datetime.desc())

        else:

            audits = Audit.query.filter(Audit.create_user == current_user).order_by(Audit.create_datetime.desc())

        if limit:

            audits = audits.limit(int(limit)).all()

        else:

            audits = audits.all()

        data_dict = dict()

        data_dict["audits"] = [audit.to_dict(6) for audit in audits]

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
