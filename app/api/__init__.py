# -*- coding: utf-8 -*-

"""

    zhifang.app.api
    ~~~~~~~~~~~~~~~

    stamaimer 02/22/17

"""


from flask import Blueprint, jsonify

from flask_security import auth_token_required


api = Blueprint("api", __name__)


@api.errorhandler(404)
def not_found(e):

    return jsonify(None), 404


@api.route("/test")
@auth_token_required
def test():

    data_dict = dict(key1="value1", key2="value2")

    return jsonify(data_dict)
