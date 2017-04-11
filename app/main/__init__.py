# -*- coding: utf-8 -*-

"""

    zhifang.app.main
    ~~~~~~~~~~~~~~~~

    stamaimer 03/13/17

"""


from subprocess import call

from flask import Blueprint, current_app, send_file

from flask_security import http_auth_required


main = Blueprint("main", __name__)


@main.route('/')
def index():

    return '', 204


@main.route("/analysis")
@http_auth_required
def analysis():

    target_filename = current_app.static_folder + "/analysis.html"

    command = "./analysis.sh"

    call([command])

    return send_file(target_filename)
