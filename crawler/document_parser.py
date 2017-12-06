#!/usr/bin/env python
# -*- coding: utf-8 -*-
from html import unescape
# from html.parser import HTMLParser
from typing import List, Union

from crawler import page_parser
from util.logger import logger

__version__ = "$"


# global connect
def getFilelist(mode = None, data = str(), parseRoot = str(), rootAttr = dict(), element = str(), attr = dict(),
                encode = 'utf8'):
    # type: (Union(str, None), str, str, dict, str, dict, Union(str, None)) -> List[(str, List)]
    # todo: 함수명을 변경한다
    # todo: result로 [[title:str(), element:list()],...]의 list를 반환하도록 한다.(title을 추가 반환->folder 이름으로 삼을 수 있도록)

    logger.debug("-* length of data: {}".format(len(data)))
    if encode is not None:
        data = data.encode(encode)

    page = page_parser.parse(data)
    root1 = parseRoot
    rootAttr1 = rootAttr
    element1 = element
    attr1 = attr

    if mode is None:
        if page.page.rss is not None:
            mode = "rss"
        else:
            mode = "html"

    if mode == "rss":
        root1 = ''
        rootAttr1 = dict()
        element1 = "item"
        attr1 = dict()

    logger.debug(root1, rootAttr1, element1, attr1)
    results = page.findElementsExt(root1, rootAttr1, element1, attr1)
    logger.debug("-* length of parse: {}".format(len(results)))
    # print results

    if mode == "rss":
        # hp = HTMLParser()
        targets = results
        results = list()
        for iter in targets:
            logger.debug("-* string of description : {}".format(iter.description.string))
            # data = hp.unescape(iter.description.string)
            data = unescape(iter.description.string)
            result = getFilelist("item", data, parseRoot, rootAttr, element, attr, encode = None)
            results.extend(result)
        pass
    logger.debug("-* type of result : ({})[0]{}".format(len(results), type(results[0])))

    return results
