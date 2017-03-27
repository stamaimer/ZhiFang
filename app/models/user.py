# -*- coding: utf-8 -*-

"""

    zhifang.app.models.user
    ~~~~~~~~~~~~~~~~~~~~~~~

    stamaime 02/22/17

"""


from flask_security import UserMixin

from . import db, roles_users, specialties_users, AppModel


class User(AppModel, UserMixin):

    employee_no = db.Column(db.Integer(), unique=1)  # 工号

    id_no = db.Column(db.String(128), unique=1)  # 身份证号

    email = db.Column(db.String(128), unique=1)  # 邮箱 不填

    phone = db.Column(db.String(128), unique=1, nullable=0)  # 手机

    image = db.Column(db.String(128))  # 签名

    active = db.Column(db.Boolean(), default=1)  # 状态 默认有效

    gender = db.Column(db.Enum(u"男", u"女"))  # 性别

    username = db.Column(db.String(128), nullable=0)  # 姓名

    password = db.Column(db.String(128), nullable=0)  # 密码

    notation = db.Column(db.Text())  # 备注

    registration_id = db.Column(db.String(64))

    region_id = db.Column(db.Integer(), db.ForeignKey("region.id"))

    region = db.relationship("Region", foreign_keys=region_id)

    roles = db.relationship("Role", secondary=roles_users,
                            backref=db.backref("users", lazy="dynamic"))

    specialties = db.relationship("Specialty", secondary=specialties_users)

    def __init__(self, phone="", username="", password="", region=None, roles=[]):

        self.username = username

        self.password = password

        self.region = region

        self.phone = phone

        self.roles = roles

    def __repr__(self):

        return self.username
