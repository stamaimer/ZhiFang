# -*- coding: utf-8 -*-

"""

    zhifang.app.api.clock
    ~~~~~~~~~~~~~~~~~~~~~

    stamaimer 02/28/17

"""


import traceback

from flask import abort, current_app, jsonify, request

from flask_security import auth_token_required, current_user

from app.models.clock import Clock

from . import api


@api.route("/clock", methods=["POST"])
@auth_token_required
def create_clock():

    try:

        request_json = request.get_json(force=1)

        notation = request_json.get("notation")

        position = request_json.get("position")

        project_id = request_json.get("project_id")

        clock = Clock(notation, position, project_id, current_user.id)

        clock.save()

        data_dict = dict(clock_id=clock.id)

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
