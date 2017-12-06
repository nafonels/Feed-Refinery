#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from urllib import parse as urlparse

from bs4 import BeautifulSoup

from util.logger import logger

__version__ = "$"

_LONG_PAGE_LENGTH = 90000


def parse(page, encoding = None):
    return ParsedPage(page, encoding)
    # return object()
    # pass


class ParsedPage(object):
    def __init__(self, page, encoding = None):
        super(ParsedPage, self).__init__()
        if encoding is not None:
            self.orig_page = page.decode(encoding, 'ignore')  # .encode()

            # print(page)
            # print(encoding, self.page.original_encoding)
        if isinstance(page, str):
            if len(page) > _LONG_PAGE_LENGTH:
                logger.warning(" Page type is Str, but too long. auto converted and continue from str() to bytes()")
                page = page.encode()
        self.page = BeautifulSoup(page)  # , "lxml")  # , from_encoding = encoding)
        self.original_encoding = self.page.original_encoding

        # meta tag가 있을 경우 charset를 찾을 수 있다
        # encode = self.findAttributefromElements('','meta','charset')
        # # print('charset1:', encode)
        # if encode == []:
        #     content = self.findAttributefromElements('','meta','content')
        #     # print ('charset',content)
        #     for iter in content:
        #         if iter.find("charset") != -1: encode.append(iter[iter.rfind("charset")+8:])
        #             # print(iter[iter.find("charset")+8:])
        # # else:
        #     # print('charset2:', encode)

        # if encode == []:
        #     encode.append('UTF-8')
        #     # print(page)
        # # print (encode)

        # # print(encode[0])
        # print (page.encode(encode[0]).decode('utf8'))
        # self.page = BeautifulSoup(page, from_encoding = encode[0])

    def findElements(self, root = str(), target = str(), _global = False):
        rootparse = self.mappingAttr(root)
        targetparse = self.mappingAttr(target)
        # r1 = re.compile(r"(?P<e>[^.#]+)#?(?P<id>[^.#]*)\.?(?P<c>[^.#]*)")
        # rootparse = r1.match(re.sub(r"([^.#]+)(\.[^.#]+)(.+)", r"\1\3\2", root)).groupdict()
        # t = [key for key, val in rootparse.items() if len(val) == 0]    # filter(lambda i:len(i[1])==0)

        # for key in t:
        #     rootparse[key] = None

        # r2 = re.compile(r"([^[]+)\[(.+)\]")  # ])
        # try:
        #     rootparse['e'], attrs = re.match(r2, rootparse['e']).groups()
        #     for i, j in [i.split('=') for i in attrs.split(',')]:
        #         rootparse[i] = j
        # except AttributeError:
        #     pass

        # ret = self.page.find(rootparse['e'], id=rootparse['id'], class_=rootparse['class']).findAll(target)
        # ret = self.page.find(rootparse['e'], {"id":rootparse['id'],"class":rootparse['class']}).findAll(target)
        # print rootparse
        # print targetparse
        try:
            # ret = self.page.find(rootparse.pop('e'), rootparse).findAll(targetparse.pop('e'), targetparse)

            # temp = rootparse['e']
            # print self.find(, rootparse)
            ret = self.findElementsExt(rootparse.pop('e'), rootparse, targetparse.pop('e'), targetparse, _global)
            # print ret
        except AttributeError:
            ret = BeautifulSoup("Not Parsed")
            raise

        return ret

    def findElementsExt(self, root = None, rootattr = dict(), target = None, targetattr = dict(), _global = False):
        # print self.page.find(root, rootattr)
        if (root is None or len(root) == 0) and rootattr == {}:
            ret = self.pagef.page.findAll(target, targetattr)
        elif _global is False:
            ret = self.page.find(root, rootattr).findAll(target, targetattr)
        else:
            ret = list()
            for iter in self.page.findAll(root, rootattr):
                ret.extend(iter.findAll(target, targetattr))
        return ret

    def findAttributefromElements(self, root, target, attr, _global = False):
        elements = self.findElements(root, target, _global)
        # ret = [i._getAttrMap()[attr] for i in elements]
        # ret = [i.attrs[attr] for i in elements]
        ret = list()
        for i in elements:
            att = i.attrs.get(attr)
            if att is not None: ret.append(att)

        return ret

    def mappingAttr(self, s = str()):
        if s == '':
            return {'e': None}

        r2 = re.compile(r"([^[]+)\[(.+)\]")  # ])")
        ret = dict()

        try:
            s, attrs = re.match(r2, s).groups()
            for i, j in [i.split('=') for i in attrs.split(',')]:
                ret[i.strip()] = j.strip()
        except AttributeError:
            pass

        r1 = re.compile(r'(?P<e>[^.#]+)#?(?P<id>[^.#]*)\.?(?P<class>[^.#]*)')
        res = r1.match(re.sub(r"([^.#]+)(\.[^.#]+)(#.+)", r"\1\3\2", s)).groupdict()
        for key, val in res.items():
            if len(val) == 0:
                val = None
            ret[key] = val
            # t = [key for key, val in ret.items() if len(val) == 0]    # filter(lambda i:len(i[1])==0)

            # for key in t:
            #   ret[key] = None

        return ret

    def select(self, s = str()):
        return self.page.select(s)


def getFullurl(base, rel):
    return urlparse.urljoin(base, rel)