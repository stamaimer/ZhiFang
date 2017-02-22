# -*- coding: utf-8 -*-

"""

    zhifang.instance.config
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 02/22/17

"""


import os


SECRET_KEY = os.urandom(47)

SECURITY_PASSWORD_SALT = 'something_super_secret_change_in_production'

DB = "mysql"

DB_DRIVER = "mysqldb"

DB_USER = "stamaimer"
DB_PSWD = "123456"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "zhifang"

SQLALCHEMY_DATABASE_URI = "{db}+{db_driver}://{db_user}:{db_pswd}@{db_host}:{db_port}/{db_name}".format(db=DB,
                                                                                                        db_driver=DB_DRIVER,
                                                                                                        db_user=DB_USER,
                                                                                                        db_pswd=DB_PSWD,
                                                                                                        db_host=DB_HOST,
                                                                                                        db_port=DB_PORT,
                                                                                                        db_name=DB_NAME)