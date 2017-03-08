# -*- coding: utf8 -*-

"""

    zhifang.run
    ~~~~~~~~~~~

    stamaimer 02/22/17

"""


from app import create_app


app = create_app("config.Config")


if __name__ == '__main__':

    app.run(host=app.config["HOST"], port=app.config["PORT"], threaded=1)
