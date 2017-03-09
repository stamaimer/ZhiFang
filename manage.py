# -*- coding: utf-8 -*-

"""

    zhifang.manage
    ~~~~~~~~~~~~~~

    stamaimer 02/22/17

"""


import MySQLdb

from flask import current_app

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app.models import db
from app.models.user import User

from app import create_app


app = create_app("config.Config")

manager = Manager(app)

migrate = Migrate(app, db)


def make_shell_context():

    return dict(app=app, db=db, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))

manager.add_command("db", MigrateCommand)


@manager.command
def rebuild_db():

    connection = MySQLdb.connect(host=current_app.config["DB_HOST"],
                                 user=current_app.config["DB_USER"],
                                 passwd=current_app.config["DB_PSWD"])

    cursor = connection.cursor()

    cursor.execute("drop database if exists %s" % current_app.config["DB_NAME"])

    cursor.execute(
        "create database if not exists %s character set utf8 collate utf8_general_ci" % current_app.config["DB_NAME"])

    db.create_all()


if __name__ == "__main__":

    manager.run()
