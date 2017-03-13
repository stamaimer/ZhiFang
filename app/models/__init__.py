# -*- coding: utf-8 -*-

"""

    zhifang.app.models
    ~~~~~~~~~~~~~~~~~~

    stamaimer 02/22/17

"""


from sqlalchemy.sql import func

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class AppModel(db.Model):

    __abstract__ = 1

    __table_args__ = {"mysql_engine": "InnoDB"}

    id = db.Column(db.Integer(), primary_key=True)

    create_datetime = db.Column(db.DateTime(), default=func.now())

    update_datetime = db.Column(db.DateTime(), default=func.now())

    def save(self):

        db.session.add(self)

        db.session.commit()

    def to_dict(self, depth=5):

        if depth:

            depth -= 1

            exclude = ["active", "email", "password", "registration_id"]

            columns = [item for item in self.__table__.columns.keys() if item not in exclude]

            relationships = [item for item in self.__mapper__.relationships.keys()]

            dictionary = {column: getattr(self, column) for column in columns}

            for relationship in relationships:

                related = getattr(self, relationship)

                if related:

                    is_list = self.__mapper__.relationships[relationship].uselist

                    if is_list:

                        dictionary[relationship] = [record.to_dict(depth) for record in related]

                    else:

                        dictionary[relationship] = related.to_dict(depth)

            return dictionary


roles_users = db.Table("roles_users",
                       db.Column("role_id", db.Integer(), db.ForeignKey("user.id")),
                       db.Column("user_id", db.Integer(), db.ForeignKey("role.id")))

specialties_users = db.Table("specialties_users",
                             db.Column("specialty_id", db.Integer(), db.ForeignKey("specialty.id")),
                             db.Column("user_id", db.Integer(), db.ForeignKey("user.id")))


from .role import Role
from .user import User
from .loan import Loan
from .work import Work
from .audit import Audit
from .clock import Clock
from .leave import Leave
from .region import Region
from .project import Project
from .bulletin import Bulletin
from .work_type import WorkType
from .specialty import Specialty
from .audit_item import AuditItem
from .audit_view import AuditView
from .leave_type import LeaveType
from .project_stage import ProjectStage
from .reimbursement import Reimbursement
from .reimbursement_type import ReimbursementType
