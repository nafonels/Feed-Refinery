# !/usr/bin/env python
# -*- coding: utf-8 -*-
from http import client
from urllib.response import addinfourl

from util.logger import logger

__version__ = "$Revision$"

__supertype = bytes


class responsedString(__supertype):
    # class responsedString(bytes):
    def __new__(cls, res, s = str()):
        logger.debug("* responsedString.__new__(res: {typeofres} - {idofres}),"
                     " s: {typeofs} - {idofs})".format_map({'typeofres': type(res),
                                                            'idofres':   id(res),
                                                            'typeofs':   type(s),
                                                            'idofs':     id(s)}))
        info = None

        if isinstance(res, addinfourl):
            info = res.info()
            s = res.read()

        elif isinstance(res, client.HTTPMessage):
            info = res
            s = res.__str__
            #    #client.HttpMessage와 상동인지는 알 수 없음
        elif isinstance(res, client.HTTPResponse):
            info = res
            s = res.read()
        else:
            raise TypeError

        # 지역 변수 s가 obj의 내용으로 할당됨
        ret = super(responsedString, cls).__new__(cls, s)
        logger.debug("*- return responsedString.__new__() : {} - s.__str__() == ret.__str__() : {},".format(
                type(ret), s.__str__() == ret.__str__()))

        ret.info = info
        return ret

    def __init__(self, res):
        logger.debug("* responsedString.__init__(res: {typeofres} - {idofres})".format_map({'typeofres': type(res),
                                                                                            'idofres':   id(res)}))
        # super(responsedString, self).__init__(self, res)

        pass
