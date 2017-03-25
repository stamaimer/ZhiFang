# -*- coding: utf-8 -*-

"""

    zhifang.app.api
    ~~~~~~~~~~~~~~~

    stamaimer 02/22/17

"""


import time
import traceback

from sqlalchemy.exc import IntegrityError

from flask import Blueprint, abort, current_app, jsonify, request, g

from flask_security import auth_token_required, current_user

from flask_sqlalchemy import get_debug_queries

from app.models import db
from app.models.reimbursement_type import ReimbursementType
from app.models.project_stage import ProjectStage
from app.models.leave_type import LeaveType
from app.models.specialty import Specialty
from app.models.work_type import WorkType
from app.models.project import Project
from app.models.region import Region
from app.models.role import Role
from app.models.user import User

from app.utilities import coor2addr as docoor2addr

from app import utilities


api = Blueprint("api", __name__)


@api.errorhandler(404)
def not_found(e):

    return jsonify(None), 404


@api.before_app_first_request
def init_db():

    try:

        for text in [u"差旅费用", u"招待费用", u"租车费用", u"出版费用", u"评审费用", u"房租费用", u"办公费用", u"其他费用"]:

            reimbursement_type = ReimbursementType(text)

            reimbursement_type.save()

    except IntegrityError:

        db.session.rollback()

        # current_app.logger.error(traceback.format_exc())

    try:

        for text in [u"可研", u"初设", u"施工", u"工代", u"竣工", u"归档", u"其他"]:

            project_stage = ProjectStage(text)

            project_stage.save()

    except IntegrityError:

        db.session.rollback()

        # current_app.logger.error(traceback.format_exc())

    try:

        for text in [u"年假", u"事假", u"病假", u"婚嫁", u"产假", u"陪产假", u"调休假", u"护理假", u"其他"]:

            leave_type = LeaveType(text)

            leave_type.save()

    except IntegrityError:

        db.session.rollback()

        # current_app.logger.error(traceback.format_exc())

    try:

        for text in [u"开会", u"收资", u"内业", u"外业", u"评审", u"工代", u"其他"]:

            work_type = WorkType(text)

            work_type.save()

    except IntegrityError:

        db.session.rollback()

        # current_app.logger.error(traceback.format_exc())

    try:

        for text in [u"送电电气", u"送电结构", u"变电一次", u"变电二次", u"系统规划",
                     u"勘测", u"配网", u"技经", u"土建", u"通信", u"其他"]:

            specialty = Specialty(text)

            specialty.save()

    except IntegrityError:

        db.session.rollback()

        # current_app.logger.error(traceback.format_exc())

    try:

        role = Role("admin", "administrator")

        role.save()

    except IntegrityError:

        db.session.rollback()

        # current_app.logger.error(traceback.format_exc())

    try:

        user = User(phone="a123456", username=u"杨好三", password="123456", roles=[role])

        user.save()

        # project = Project(no="XMBH", name=u"测试项目", charge_user=user)
        #
        # project.save()

        for text in [u"广西", u"贵阳", u"西南"]:

            region = Region(text, user)

            region.save()

            user.region = region

        for index, username, text in zip([0, 1, 2, 3], [u"唐剑", u"彭朝辉", u"黄福水", u"段汝霞"], [u"四川", u"重庆", u"云南", u"西藏"]):

            user = User(phone="a123456" + str(index), region=region, username=username, password="123456", roles=[])

            user.save()

            region = Region(text, user)

            region.save()

        region = Region(u"海南", User.query.filter_by(username=u"黄福水").first())

        region.save()

    except IntegrityError:

        db.session.rollback()

        # current_app.logger.error(traceback.format_exc())


@api.before_app_request
def before_app_request():

    g.start = time.clock()

    # current_app.logger.debug("request path: " + request.url)
    #
    # current_app.logger.debug("request head: " + request.headers.__str__())
    #
    # current_app.logger.debug("request args: " + request.args.__str__())
    #
    # current_app.logger.debug("request form: " + request.form.__str__())
    #
    # current_app.logger.debug("request data: " + request.data.__str__())


@api.after_app_request
def after_app_request(response):

    # for query in get_debug_queries():
    #
    #     if query.duration * 1000 > 1:
    #
    #         current_app.logger.debug(query)

    current_app.logger.debug(time.clock() - g.start)

    return response


@api.route("/coor2addr")
@auth_token_required
def coor2addr():

    try:

        lat = request.args.get("lat")

        lon = request.args.get("lon")

        address = docoor2addr(lat, lon)

        if address:

            return jsonify(dict(address=address))

        else:

            return '', 404

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)


from .reimbursement import *
from .attachment import *
from .attendance import *
from .audit_item import *
from .audit_view import *
from .utilities import *
from .bulletin import *
from .project import *
from .audit import *
from .clock import *
from .leave import *
from .work import *
from .loan import *
from .user import *
