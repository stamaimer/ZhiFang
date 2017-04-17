# -*- coding: utf-8 -*-

"""

    zhifang.app.api.bulletin
    ~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/07/17

"""


import traceback

from flask import abort, current_app, jsonify, request

from flask_security import auth_token_required, current_user

from app.models.bulletin import Bulletin

from . import api


@api.route("/bulletin")
@auth_token_required
def select_bulletin():

    try:

        page = request.args.get("page", default=1, type=int)

        page_size = request.args.get("page_size", default=5, type=int)

        bulletins = Bulletin.query\
            .filter(Bulletin.status == 1, Bulletin.authorized_users.any(id=current_user.id))\
            .order_by(Bulletin.create_datetime.desc())\
            .paginate(page, page_size, 0).items

        data_dict = dict(bulletins=[bulletin.to_dict() for bulletin in bulletins])

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500, traceback.format_exc())
