# -*- coding: utf-8 -*-

"""

    zhifang.app
    ~~~~~~~~~~~

    stamaimer 02/22/17

"""


from flask import Flask

from flask_cors import CORS


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

    CORS(app)

    from models import db

    db.init_app(app)

    from security import security

    security.init_app(app)

    from admin import admin

    admin.init_app(app)
    #
    # from main import main as main_blueprint
    #
    # app.register_blueprint(main_blueprint)
    #
    from api import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app
