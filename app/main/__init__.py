# -*- coding: utf-8 -*-

"""

    zhifang.app.main
    ~~~~~~~~~~~~~~~~

    stamaimer 03/13/17

"""


import traceback

from subprocess import call

from flask import Blueprint, abort, current_app, render_template, send_file

from flask_security import http_auth_required, login_required

from app.models.loan import Loan
from app.models.user import User

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


@main.route("/arabic2cn/<float:amount>")
def arabic2cn(amount):

    return str(amount)


@main.route("/certificate/<int:id>")
@login_required
def generate_loan_certificate(id):

    try:

        loan = Loan.query.get(id)

        # manager = User.query.filter_by(username=u"杨好三").first()
        #
        # return render_template("certificate.html", loan=loan, manager=manager)

        if loan.status == u"已通过":

            manager = User.query.filter_by(username=u"杨好三").first()

            return render_template("certificate.html", loan=loan, manager=manager)

        else:

            return "<html>" \
                   "    <head>" \
                   "        <script>" \
                   "            alert('当前借款还未通过审批');history.go(-1);" \
                   "        </script>" \
                   "    </head>" \
                   "</html>"

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
