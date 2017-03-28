# -*- coding: utf-8 -*-

"""

    zhifang.tests
    ~~~~~~~~~~~~~

    stamaimer 03/28/17

"""


import os
import unittest
import tempfile

from app import create_app


class AppTestCase(unittest.TestCase):

    def setUp(self):

        app = create_app("config.Config")

        self.db_fd,