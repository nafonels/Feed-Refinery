#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from setting import database

__version__ = "$"

from sqlalchemy import create_engine


db_uri = URL(**database)
engine = create_engine(db_uri)

db_session = scoped_session(sessionmaker(autocommit = False,
                                         autoflush = False,
                                         bind = engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from model import ruleset, feed, item, buildinfo
    Base.metadata.create_all(bind = engine)