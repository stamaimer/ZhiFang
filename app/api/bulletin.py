# -*- coding: utf-8 -*-

"""

    zhifang.app.api.bulletin
    ~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/07/17

"""


import traceback

from flask import abort, current_app, jsonify

from flask_security import auth_token_required, current_user

from app.models.bulletin import Bulletin

from . import api


@api.route("/bulletin")
@auth_token_required
def select_bulletin():

    try:

        bulletins = Bulletin.query.all()

        data_dict = dict(bulletins=[bulletin.to_dict(1) for bulletin in bulletins])

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
