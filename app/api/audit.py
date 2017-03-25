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

        page = request.args.get("page", default=1, type=int)

        page_size = request.args.get("page_size", default=5, type=int)

        if type:

            audits = Audit.query.filter(Audit.create_user == current_user, Audit.type.op("regexp")('|'.join(type)))\
                .order_by(Audit.create_datetime.desc())

        else:

            audits = Audit.query.filter(Audit.create_user == current_user).order_by(Audit.create_datetime.desc())

        if limit:

            audits = audits.limit(int(limit)).all()

        else:

            audits = audits.all()

        data_dict = dict()

        data_dict["audits"] = [dict(id=audit.id,
                                    type=audit.type,
                                    status=audit.status,
                                    create_datetime=audit.create_datetime,
                                    update_datetime=audit.update_datetime,
                                    create_user=dict(id=audit.create_user.id, username=audit.create_user.username),
                                    audit_item=audit.audit_items[0].to_dict(2, include=["create_user", "leave_type", "project", "project_stage", "reimbursement_type", "specialty", "work_type"]),
                                    current=dict(id=audit.current.id,
                                                 advice=audit.current.advice,
                                                 status=audit.current.status,
                                                 result=audit.current.result,
                                                 audit_user=dict(id=audit.current.audit_user.id,
                                                                 username=audit.current.audit_user.username),
                                                 last=dict(id=audit.current.last.id,
                                                           advice=audit.current.last.advice,
                                                           status=audit.current.last.status,
                                                           result=audit.current.last.result,
                                                           audit_user=dict(id=audit.current.last.audit_user.id,
                                                                           username=audit.current.last.audit_user.username),
                                                           last=dict(id=audit.current.last.last.id,
                                                                     advice=audit.current.last.last.advice,
                                                                     status=audit.current.last.last.status,
                                                                     result=audit.current.last.last.result,
                                                                     audit_user=dict(id=audit.current.last.last.audit_user.id,
                                                                                     username=audit.current.last.last.audit_user.username))
                                                           if audit.current.last.last else None)
                                                 if audit.current.last else None))
                               for audit in audits]

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
