# -*- coding: utf-8 -*-

"""

    zhifang.app.utilities
    ~~~~~~~~~~~~~~~~~~~~~

    stamaimer 02/27/17

"""


import base64
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


# def coor2addr(lat, lon):
#
#     address = ""
#
#     payload = dict()
#
#     payload["key"] = current_app.config["PICK_POINT_API_KEY"]
#
#     payload["lat"] = lat
#
#     payload["lon"] = lon
#
#     payload["zoom"] = 18
#
#     payload["addressdetails"] = 0
#
#     headers = dict()
#
#     headers["accept-language"] = "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4"
#
#     try:
#
#         response = requests.get("https://api.pickpoint.io/v1/reverse", params=payload, headers=headers)
#
#         if response.ok:
#
#             address = response.json()["display_name"]
#
#         else:
#
#             current_app.logger.info(response.reason)
#
#     except:
#
#         current_app.logger.info(traceback.format_exc())
#
#     finally:
#
#         return address


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


def push(content, target="all"):

    # base64_auth_string = base64.b64encode(':'.join([
    #     current_app.config["JPUSH_APP_KEY"],
    #     current_app.config["JPUSH_MASTER_SECRET"]]))
    #
    # headers = dict()
    #
    # headers["Authorization"] = "Basic " + base64_auth_string
    #
    # headers["Content-Type"] = "application/json"
    #
    # payload = dict()
    #
    # payload["platform"] = "all"
    #
    # if target == "all":
    #
    #     payload["audience"] = target
    #
    # payload["audience"] = dict(registration_id=[target.encode("utf-8")])
    #
    # payload["notification"] = dict(alert=content.encode("utf-8"))
    #
    # current_app.logger.info(headers)
    #
    # current_app.logger.info(payload)
    #
    # try:
    #
    #     response = requests.post("https://api.jpush.cn/v3/push", headers=headers, data=str(payload))
    #
    #     current_app.logger.info(response.status_code)
    #
    #     current_app.logger.info(response.content)
    #
    # except:
    #
    #     current_app.logger.error(traceback.format_exc())

    _jpush = jpush.JPush(current_app.config["JPUSH_APP_KEY"], current_app.config["JPUSH_MASTER_SECRET"])

    _push = _jpush.create_push()

    _jpush.set_logging("DEBUG")

    if target == "all":

        _push.audience = jpush.all_

    else:

        _push.audience = jpush.audience(jpush.registration_id(target,))

    _push.notification = jpush.notification(alert=content)

    _push.options = {"apns_production": False}

    _push.platform = jpush.all_

    try:

        _push.send()

    except:

        current_app.logger.error(traceback.format_exc())
