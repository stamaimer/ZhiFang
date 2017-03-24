# -*- coding: utf-8 -*-

"""

    zhifang.app.api.bulletin
    ~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/07/17

"""


import ast
import traceback

from flask import abort, current_app, jsonify, request

from flask_security import auth_token_required, current_user

from app.models.bulletin import Bulletin

from . import api


@api.route("/bulletin")
@auth_token_required
def select_bulletin():

    try:

        limit = request.args.get("limit")

        query = Bulletin.query.filter(Bulletin.authorized_users.any(id=current_user.id))

        if limit:

            bulletins = query.order_by(Bulletin.create_datetime.desc()).limit(int(limit)).all()

        else:

            bulletins = query.order_by(Bulletin.create_datetime.desc()).all()

        data_dict = dict(bulletins=[dict(id=bulletin.id, title=bulletin.title, content=bulletin.content,
                                         image=ast.literal_eval(bulletin.image))
                                    for bulletin in bulletins])

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
