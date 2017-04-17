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
from app.models import db

from . import api


@api.route("/clock")
@auth_token_required
def select_clock():

    try:

        page = request.args.get("page", default=1, type=int)

        page_size = request.args.get("page_size", default=5, type=int)

        clocks = Clock.query.filter_by(create_user=current_user)\
            .order_by(Clock.create_datetime.desc()).paginate(page, page_size, 0).items

        data_dict = dict()

        data_dict["clocks"] = [clock.to_dict(2, include=["project"]) for clock in clocks]

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500, traceback.format_exc())


@api.route("/clock", methods=["POST"])
@auth_token_required
def create_clock():

    try:

        request_json = request.get_json(force=1)

        notation = request_json.get("notation")

        position = request_json.get("position")

        project_id = request_json.get("project_id")

        if position and project_id:

            clock = Clock(notation, position, project_id, current_user.id)

            clock.save()

            data_dict = dict(clock_id=clock.id)

            return jsonify(data_dict)

        else:

            return "Bad Request", 400

    except:

        db.session.rollback()

        current_app.logger.error(traceback.format_exc())

        abort(500, traceback.format_exc())
