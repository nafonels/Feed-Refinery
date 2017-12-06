#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import BLOB, Column, ForeignKey, Integer, UnicodeText

from model import Base
from model.util.mixin import ArgumentedTableMixin

__version__ = "$"


class Feed(ArgumentedTableMixin, Base):
    __tablename__ = "feed"
    id = Column(Integer, ForeignKey('ruleset.id'), primary_key = True)
    rss = Column(BLOB)
    atom = Column(BLOB)
    pub_date = Column(UnicodeText())
