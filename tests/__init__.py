# -*- coding: utf-8 -*-

"""

    zhifang.tests
    ~~~~~~~~~~~~~

    stamaimer 03/28/17

"""


def login(client, email, password):
    return client.post("/login", data={"email": email, "password": password}, follow_redirects=1)


def logout(client):
    return client.get("/logout", follow_redirects=1)
    