# -*- coding: utf-8 -*-

"""

    zhifang.app.api.user
    ~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/04/17

"""

import traceback

from flask import abort, current_app, jsonify, request

from flask_security import auth_token_required, current_user

from app.models import db
from app.models.user import User

from . import api


@api.route("/user", methods=["PATCH"])
@auth_token_required
def update_user():

    try:

        request_json = request.get_json(force=1)

        registration_id = request_json.get("registration_id")

        current_user.registration_id = registration_id

        db.session.commit()

        return "No Content", 204

    except:

        db.session.rollback()

        current_app.logger.error(traceback.format_exc())

        abort(500, traceback.format_exc())


@api.route("/user")
@auth_token_required
def select_user():

    try:

        role = request.args.get("role", default="general")

        users = User.query.filter(User.roles.any(name=role), User.active == 1).all()

        data_dict = dict(users=[user.to_dict() for user in users])

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500, traceback.format_exc())
