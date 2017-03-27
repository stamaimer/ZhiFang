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

        return '', 204

    except:

        db.session.rollback()

        current_app.logger.error(traceback.format_exc())

        abort(500)


@api.route("/user")
@auth_token_required
def select_user():

    try:

        users = User.query.filter_by(active=1).all()  # add filter

        data_dict = dict(users=[user.to_dict() for user in users])

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
