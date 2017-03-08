# -*- coding: utf-8 -*-

"""

    zhifang.app.api.bulletin
    ~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/07/17

"""


import traceback

from sqlalchemy.event import listens_for

from flask import abort, current_app, jsonify

from flask_security import auth_token_required, current_user

from app.models.bulletin import Bulletin

from app.utilities import push

from . import api


@api.route("/bulletin")
@auth_token_required
def select_bulletin():

    try:

        bulletins = Bulletin.query.all()

        data_dict = dict(bullets=[bulletin.to_dict(1) for bulletin in bulletins])

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)


@listens_for(Bulletin, "after_insert")
def push_after_bulletin_insert(mapper, connection, target):

    push(u"你有一条新的通知公告", "all")
