# -*- coding: utf-8 -*-

"""

    zhifang.app.api.attendance
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/14/17

"""


import traceback

from flask import abort, current_app, jsonify, request

from flask_security import auth_token_required, current_user

from app.models.clock import Clock
from app.models.leave import Leave

from . import api


@api.route("/attendance")
@auth_token_required
def select_attendance():

    try:

        page = request.args.get("page", default=1, type=int)

        page_size = request.args.get("page_size", default=5, type=int)

        clocks = Clock.query.filter_by(create_user=current_user)\
            .order_by(Clock.create_datetime.desc()).paginate(page, page_size)

        leaves = Leave.query.filter_by(create_user=current_user)\
            .order_by(Leave.create_datetime.desc()).paginate(page, page_size)

        data_dict = dict()

        data_dict["clocks"] = [dict(id=clock.id,
                                    notation=clock.notation,
                                    position=clock.position,
                                    datetime=clock.datetime,
                                    project=dict(id=clock.project.id, name=clock.project.name)) for clock in clocks]

        data_dict["leaves"] = [dict(id=leave.id,
                                    last=leave.last,
                                    status=leave.status,
                                    beg_date=leave.beg_date,
                                    end_date=leave.end_date,
                                    notation=leave.notation,
                                    create_datetime=leave.create_datetime,
                                    leave_type=dict(id=leave.leave_type.id, text=leave.leave_type.text))
                               for leave in leaves]

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
