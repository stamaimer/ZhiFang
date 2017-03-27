# -*- coding: utf-8 -*-

"""

    zhifang.config
    ~~~~~~~~~~~~~~

    stamaimer 02/22/17

"""


class Config(object):

    HOST = "127.0.0.1"

    PORT = 7070

    DEBUG = 1  # to modify

    WTF_CSRF_ENABLED = 0

    SECURITY_PASSWORD_HASH = "bcrypt"

    SECURITY_USER_IDENTITY_ATTRIBUTES = ("phone")

    SQLALCHEMY_ECHO = 0

    SQLALCHEMY_POOL_SIZE = 20

    SQLALCHEMY_POOL_RECYCLE = 10

    SQLALCHEMY_COMMIT_ON_TEARDOWN = 0

    SQLALCHEMY_TRACK_MODIFICATIONS = 1

    SENTRY_USER_ATTRS = ["username"]
