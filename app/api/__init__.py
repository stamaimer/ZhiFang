# -*- coding: utf-8 -*-

"""

    zhifang.app.api
    ~~~~~~~~~~~~~~~

    stamaimer 02/22/17

"""


from sqlalchemy.exc import IntegrityError

from flask import Blueprint, jsonify

from flask_security import auth_token_required

from app.models import db
from app.models.role import Role
from app.models.user import User


api = Blueprint("api", __name__)


@api.errorhandler(404)
def not_found(e):

    return jsonify(None), 404


@api.before_app_first_request
def init_db():

    try:

        role = Role("admin", "administrator")

        db.session.merge(role)

        db.session.commit()

        user = User("stamaimer@gmail.com", "a13886121353", 1, "stamaimer", "123456", [role])

        db.session.merge(user)

        db.session.commit()

    except IntegrityError:

        db.session.rollback()


@api.route("/test")
@auth_token_required
def test():

    data_dict = dict(key1="value1", key2="value2")

    return jsonify(data_dict)
