#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import UnicodeText

from model import Base
from model.util.mixin import ArgumentedTableMixin

__version__ = "$"


class Ruleset(ArgumentedTableMixin, Base):
    __tablename__ = "ruleset"
    id = Column(Integer, primary_key = True, autoincrement = True)
    # rule of list/page
    listUrl = Column(UnicodeText())
    encoding = Column(String())
    # feed description
    title = Column(UnicodeText())
    description = Column(UnicodeText())
    category = Column(UnicodeText())
    # rule of itemlist
    itemlink = Column(UnicodeText())
    nextpagelink = Column(UnicodeText())
    maxcheckpage = Column(Integer, default = 3)
    # rule of item
    itemtitle = Column(UnicodeText())
    itemauthor = Column(UnicodeText())
    itemcategory = Column(UnicodeText())
    itemdescription = Column(UnicodeText())
    itemguidtype = Column(UnicodeText())
    itemguidfrom = Column(UnicodeText())
    itemguid = Column(UnicodeText())
    itempub_date = Column(UnicodeText())
    itempub_date_format = Column(UnicodeText())

    # itemcomment = Column(UnicodeText())

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def make_ret(self):
        return dict(
                id = self.id,
                listUrl = self.listUrl,
                title = self.title,
                description = self.description
        )


