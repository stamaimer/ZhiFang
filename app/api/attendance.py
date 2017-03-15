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

        clocks = Clock.query.filter_by(user=current_user).all()

        leaves = Leave.query.filter_by(create_user=current_user).all()

        data_dict = dict()

        data_dict["clocks"] = [clock.to_dict(3) for clock in clocks]

        data_dict["leaves"] = [leave.to_dict(3) for leave in leaves]

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
