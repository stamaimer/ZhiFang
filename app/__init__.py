# -*- coding: utf-8 -*-

"""

    zhifang.app
    ~~~~~~~~~~~

    stamaimer 02/22/17

"""


import logging

from raven.contrib.flask import Sentry

from werkzeug.contrib.fixers import ProxyFix

from flask import Flask

from app.form import AppLoginForm


def create_app(config_name):

    """

    set up a application instance, init extensions, register blueprints

    http://flask.pocoo.org/docs/0.12/patterns/appfactories/

    Args:
        config_name: name of configuration of application instance

    Returns: a application instance

    """

    app = Flask(__name__, instance_relative_config=1)

    app.config.from_object(config_name)

    app.config.from_pyfile("config.py")

    from utilities import cors, babel

    cors.init_app(app)

    babel.init_app(app)

    from utilities.json import AppJSONEncoder

    app.json_encoder = AppJSONEncoder

    sentry = Sentry()

    sentry.init_app(app, logging=1, level=logging.ERROR)

    from models import db

    db.init_app(app)

    from security import security

    security.init_app(app)

    from admin import admin

    admin.init_app(app)

    from main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from api import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api")

    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app
