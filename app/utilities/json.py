# -*- coding: utf-8 -*-

"""

    zhifang.app.utilities.json
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/17/17

"""


from datetime import date, datetime

from flask.json import JSONEncoder


class AppJSONEncoder(JSONEncoder):

    def default(self, o):

        try:

            if isinstance(o, datetime) or isinstance(o, date):

                return str(o)

            iterable = iter(o)

        except TypeError:

            pass

        else:

            return list(iterable)

        return JSONEncoder.default(self, o)
