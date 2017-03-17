# -*- coding: utf-8 -*-

"""

    zhifang.app.utilities.json
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/17/17

"""


from datetime import datetime

from flask.json import JSONEncoder


class AppJSONEncoder(JSONEncoder):

    def default(self, o):

        try:

            if isinstance(o, datetime):

                return str(o)

            iterable = iter(o)

        except TypeError:

            pass

        else:

            return list(iterable)

        return JSONEncoder.default(self, o)
