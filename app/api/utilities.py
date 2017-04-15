# -*- coding: utf-8 -*-

"""

    zhifang.app.api.utilities
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    stamaimer 03/03/17

"""


import traceback

from flask import abort, current_app, jsonify, request

from flask_security import auth_token_required

from app.models.reimbursement_type import ReimbursementType
from app.models.project_stage import ProjectStage
from app.models.leave_type import LeaveType
from app.models.specialty import Specialty
from app.models.work_type import WorkType

from . import api


data_maps = dict(reimbursement_type=ReimbursementType, project_stage=ProjectStage,
                 leave_type=LeaveType, specialty=Specialty, work_type=WorkType, )

name_maps = dict(reimbursement_type="reimbursement_types", project_stage="project_stages",
                 leave_type="leave_types", specialty="specialties", work_type="work_types")


@api.route("/reimbursement_type/")
@api.route("/project_stage/")
@api.route("/leave_type/")
@api.route("/specialty/")
@api.route("/work_type/")
@auth_token_required
def get_utilities():

    try:

        data_type = request.path.split('/')[-1]

        items = data_maps.get(data_type).query.filter_by(status=1).all()

        data_dict = dict()

        data_dict[name_maps.get(data_type)] = [item.to_dict() for item in items]

        return jsonify(data_dict)

    except:

        current_app.logger.error(traceback.format_exc())

        abort(500)
