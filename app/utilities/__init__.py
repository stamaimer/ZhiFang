# -*- coding: utf-8 -*-

"""

    zhifang.app.utilities
    ~~~~~~~~~~~~~~~~~~~~~

    stamaimer 02/27/17

"""


import traceback

import requests

import jpush

from flask import current_app, request, session

from flask_cors import CORS

from flask_babelex import Babel


cors = CORS()

babel = Babel()


@babel.localeselector
def get_locale():

    """

    get the language argument from request

    Returns:

    """

    if request.args.get("lang"):

        session["lang"] = request.args.get("lang")

    return session.get("lang", "zh_CN")


def coor2addr(lat, lon):

    address = ""

    payload = dict()

    payload["coordtype"] = "wgs84ll"

    payload["location"] = ','.join([lat, lon])

    payload["output"] = "json"

    payload["ak"] = current_app.config["BAIDU_MAP_API_AK"]

    try:

        response = requests.get("http://api.map.baidu.com/geocoder/v2/", params=payload)

        if response.ok:

            data = response.json()

            if data["status"] == 0:

                address = data["result"]["formatted_address"]

            else:

                current_app.logger.error(data["status"])

        else:

            current_app.logger.error(response.reason)

    except:

        current_app.logger.error(traceback.format_exc())

    finally:

        return address


def push(content, *target):

    _jpush = jpush.JPush(current_app.config["JPUSH_APP_KEY"], current_app.config["JPUSH_MASTER_SECRET"])

    _push = _jpush.create_push()

    _jpush.set_logging("DEBUG")  # to modify

    if target:

        _push.audience = jpush.audience(jpush.registration_id(target))  # to test

    else:

        _push.audience = jpush.all_

    _push.notification = jpush.notification(alert=content)

    _push.options = {"apns_production": 0}  # to modify

    _push.platform = jpush.all_

    try:

        _push.send()

    except:

        current_app.logger.error(traceback.format_exc())
