#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, UnicodeText

from model import Base
from model.util.mixin import ArgumentedTableMixin

__version__ = "$"


class BuildInfo(ArgumentedTableMixin, Base):
    __tablename__ = "build_info"
    id = Column(Integer, ForeignKey('ruleset.id'), primary_key = True)
    check_interval = Column(Integer)
    last_builddate = Column(UnicodeText())
    pub_date = Column(UnicodeText())
