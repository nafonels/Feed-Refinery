#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, UnicodeText

from model import Base
from model.util.mixin import ArgumentedTableMixin

__version__ = "$"


class Item(ArgumentedTableMixin, Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key = True, autoincrement = True)
    feedid = Column(Integer, ForeignKey('ruleset.id'))
    title = Column(UnicodeText())
    link = Column(UnicodeText())
    author = Column(UnicodeText())
    category = Column(UnicodeText())
    description = Column(UnicodeText())
    guid = Column(UnicodeText())
    pub_date = Column(UnicodeText())
    comment = Column(UnicodeText())
