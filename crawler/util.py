#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crawler.http_opener import make_absolute_uri

__version__ = "$Revision$"


def get_absolute_anchor_reference(abspath, selected):
    # print("abs : %s + %s", abspath, selected)
    return make_absolute_uri(abspath, get_anchor_reference(selected))


def get_anchor_reference(selected):
    # print(selected)
    # print(type(selected))
    if selected.name == 'a':
        return selected.attrs['href']
    else:
        return selected.find('a').attrs['href']


def regsub(url, pattern, repl):
    import re
    return re.sub(pattern, repl, url)


def make_CDATA(s):
    return ''.join(["<![CDATA[", s, "]]>"])
