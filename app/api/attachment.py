# -*- coding: utf-8 -*-

"""

    zhifang.app.api.attachment
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/14/17

"""


import re
import traceback

from flask import abort, current_app

from app.models import AuditItem

from . import api


@api.route("/attachment/<int:id>.jpeg")
def select_attachment(id):

    try:

        audit_item = AuditItem.query.get(id)

        if audit_item and audit_item.attachment:

                return re.sub("data:image/jpeg;base64,", '', audit_item.attachment).decode("base64"), \
                       {"content-type": "image/jpeg"}

        else:

            return "Not Found", 404

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500, traceback.format_exc())
