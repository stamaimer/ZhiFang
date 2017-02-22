# -*- coding: utf-8 -*-

"""

    zhifang.app.models
    ~~~~~~~~~~~~~~~~~~

    stamaimer 02/22/17

"""


from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

roles_users = db.Table("roles_users",
                       db.Column("role_id", db.Integer(), db.ForeignKey("user.id")),
                       db.Column("user_id", db.Integer(), db.ForeignKey("role.id")))
