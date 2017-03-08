# -*- coding: utf-8 -*-

"""

    zhifang.app.api.utilities
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/03/17

"""


import traceback

from flask import abort, current_app, jsonify

from app.models.reimbursement_type import ReimbursementType
from app.models.project_stage import ProjectStage
from app.models.leave_type import LeaveType
from app.models.specialty import Specialty
from app.models.work_type import WorkType

from . import api


@api.route("/reimbursement_type")
def get_reimbursement_type():

    try:

        reimbursement_types = ReimbursementType.query.all()

        data_dict = dict()

        data_dict["reimbursement_types"] = [reimbursement_type.to_dict()
                                           for reimbursement_type in reimbursement_types]

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)


@api.route("/project_stage")
def get_project_stage():

    try:

        project_stages = ProjectStage.query.all()

        data_dict = dict()

        data_dict["project_stages"] = [project_stage.to_dict() for project_stage in project_stages]

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)


@api.route("/leave_type")
def get_leave_type():

    try:

        leave_types = LeaveType.query.all()

        data_dict = dict()

        data_dict["leave_types"] = [leave_type.to_dict() for leave_type in leave_types]

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)


@api.route("/specialty")
def get_specialty():

    try:
        specialties = Specialty.query.all()

        data_dict = dict()

        data_dict["specialties"] = [specialty.to_dict() for specialty in specialties]

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)


@api.route("/work_type")
def get_work_type():

    try:

        work_types = WorkType.query.all()

        data_dict = dict()

        data_dict["work_types"] = [work_type.to_dict() for work_type in work_types]

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
