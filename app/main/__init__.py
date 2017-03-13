# -*- coding: utf-8 -*-

"""

    zhifang.app.main
    ~~~~~~~~~~~~~~~~

    stamaimer 03/13/17

"""


from flask import Blueprint


main = Blueprint("main", __name__)


@main.route('/')
def index():

    return '', 204
