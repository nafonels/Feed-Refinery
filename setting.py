#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "$"

channel = "devel"

if channel == "devel":
    import os
    _PROJ_ROOT = os.path.dirname(os.path.realpath(__file__))
    database = {
        "drivername" : "sqlite",
        "database" : os.path.join(_PROJ_ROOT, 'tmp', 'flaskdb.db')
    }
    logfile = os.path.join(_PROJ_ROOT, 'tmp', "logfile.log")

if channel == "test":
    database = {
        "drivername" : "postgresql",
        "host" : "db",
        "port" : "5432",
        "database" : "postgres",
        "username" : "postgres",
        "password" : "mysecretpassword"
    }