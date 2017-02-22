# -*- coding: utf-8 -*-

"""

    zhifang.manage
    ~~~~~~~~~~~~~~

    stamaimer 02/22/17

"""


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


if __name__ == "__main__":

    manager.run()
