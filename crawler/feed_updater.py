#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from datetime import datetime

from crawler import page_parser
from crawler.http_opener import makeOpenerWithoutCookie, openPage
from crawler.scheduler import scheduler
from crawler.util import get_absolute_anchor_reference, make_CDATA, regsub
from model import db_session
from model.buildinfo import BuildInfo
from model.item import Item
from model.ruleset import Ruleset
from util.logger import logger

__version__ = "$Revision$"


def update(feedid: int) -> bool:
    buildinfo = BuildInfo.return_item(feedid)
    scheduler.add_job(update, 'interval', args = [feedid], id = 'feed{}'.format(feedid), replace_existing = True,
                      minutes = int(buildinfo.check_interval)
                      )

    rule = Ruleset.return_item(feedid)  # type : Ruleset
    _rmodified = False
    # print("Auth:", rset.getauth, rset.auth1, rset.auth1param)
    # if rset.getauth != '':
    #     _auth = {rset.auth1: rset.auth1param, rset.auth2: rset.auth2param,
    #              rset.auth3: rset.auth3param, rset.auth4: rset.auth4param,
    #              rset.auth5: rset.auth5param, }
    #
    #     makeOpenerWithCookie(rset.getauth, _auth)
    # else:
    makeOpenerWithoutCookie(rule.listUrl)

    # optional
    encoding = rule.encoding
    if encoding == '': encoding = 'utf-8'

    if not rule.maxcheckpage or rule.maxcheckpage < 1:
        logger.warning("*- rset.maxcheckpage is None, set default")
        maxpage = 1
    else:
        maxpage = rule.maxcheckpage

    if not rule.nextpagelink or not len(rule.nextpagelink):
        maxpage = 1

    logger.info("*- feed initializing....: feed_no. {}".format(feedid))

    item_list, listpage = get_pageitems(rule, maxpage, encoding)

    list_url = rule.listUrl
    item_list = list(map((lambda i: get_absolute_anchor_reference(list_url, i)), item_list))

    if rule.encoding == '':
        rule.encoding = listpage.original_encoding
        _rmodified = True

    # update_feed and update BuildInfo.lastBuildDate
    if update_feed(feedid, rule, item_list):
        buildinfo.lastBuildDate = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
    else:
        logger.error("feed 생성에 실패하였음")
        return False
    # whether not updated feed(list not updated), change pub_date
    buildinfo.pub_date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())

    if _rmodified:
        # rule.save()

        db_session.commit()
    return True


def get_pageitems(rule, maxpage = 1, encoding = 'utf-8'):
    list_url = rule.listUrl
    item_list = list()
    page_count = 0

    # end loop : 1 < 1 -> False
    while page_count < maxpage:
        logger.debug("*- loop {}/{} - encoding: ({}) {}"
                     .format(page_count + 1, maxpage, len(rule.encoding), rule.encoding))

        # _page = openPage(listurl).decode(encoding, 'ignore')
        _page = openPage(list_url)  # bytes
        if encoding != 'utf-8':
            _t1 = _page.rfind(b"<meta", 0, _page.find(b"charset"))
            _t2 = _page.find(b'>', _t1) + 1
            page = _page[:_t1] + _page[_t2:]
        else:
            page = _page
        # item_list 가 초기화되지 않음
        # logger.info("*- list(encoding:{encoding}, listpage: {list_len}(|{listpage}|), item:{item_len})"
        #             .format_map({'encoding': encoding, 'list_len': len(_page), 'listpage': _page[:13].decode(encoding),
        #                          'item_len': len(item_list)}))
        logger.info("*- list(encoding:{encoding}, listpage: {list_len}(|{listpage}|))"
                    .format_map({'encoding': encoding, 'list_len': len(_page), 'listpage': _page[:13].decode(encoding),
                                 }))

        listpage = page_parser.parse(page)
        items = listpage.select(str(rule.itemlink))
        item_list.extend([iter for iter in items if iter not in item_list])

        logger.info("*- item {item_len}, (listpage loaded: {listpage}, get_itemlink: {getlink})"
                    .format_map({'count':   page_count + 1, 'listpage': len(str(listpage.page)) > 0,
                                 'getlink': len(items) > 0, 'item_len': len(item_list)}))

        nextpages = listpage.select(str(rule.nextpagelink))
        logger.debug("*- nextpage:{} - {}({})"
                     .format(str(rule.nextpagelink), (len(nextpages) > 0), nextpages))
        if len(nextpages):  # relative url -> absolute url
            _listurl = get_absolute_anchor_reference(str(rule.listUrl), nextpages[0])
            if list_url == _listurl: break
            list_url = _listurl
        else:
            break

        page_count = page_count + 1
    return item_list, listpage


def update_feed(feedid, rset, itemlist: list):
    # cleanup list of new feeds
    _itemlist = itemlist.copy()  # list of new item's links
    olditems = Item.query.filter(Item.feedid == feedid).all()  # list of old items in feed
    for iter in olditems:
        if str(iter.link) in _itemlist: _itemlist.remove(iter.link)

    # 새 feed가 없고, 이전에도 feed가 없었던 경우
    if (len(_itemlist) == 0) and (len(itemlist) == len(olditems)):
        return False

    # delete all old feed items
    # todo: feed별 삭제여부를 지정할 수 있도록 할 것
    logger.debug("remove all old items in feed: {}".format(feedid))
    for olditem in olditems:
        db_session.delete(olditem)

    count = 1
    for iter in itemlist:
        logger.info("processing...: {count} / {length}".format_map({'count': count, 'length': len(itemlist)}))
        count = count + 1

        feeditem = update_feeditem(feedid, iter, rset)
        if feeditem:
            db_session.add(feeditem)
    db_session.commit()
    return True
    # except:
    #     return False


def update_feeditem(feedid, iter, rset):
    con = openPage(iter)

    if not (rset.encoding) or len(rset.encoding) == 0:
        encoding = 'utf-8'
    else:
        encoding = str(rset.encoding)

    page = page_parser.parse(con, encoding = str(encoding))
    logger.debug("*- page<{encoding}> : ({pagelength}){itempage}"
                 .format_map({'encoding': encoding, 'pagelength': len(con),
                              'itempage': con[:14].decode(encoding)}))
    # todo: tbody가 inspector에는 나오지만 tbody가 없는 경우도 있다는 점을 주의하라고 쓰자.
    # todo : 참조 https://hexfox.com/p/having-trouble-extracting-the-tbody-element-during-my-web-scrape/

    try:
        title = make_CDATA(page.select(rset.itemtitle)[0].get_text())
        logger.debug("*- title: <{}> {}".format(str(rset.itemtitle), title))
        link = make_CDATA(iter)
        logger.debug("*- link: {}".format(link))
        desc = make_CDATA(page.select(rset.itemdescription)[0].prettify(formatter = "minimal"))
        logger.debug("*- desc: <{}>({}) {}".format(rset.itemdescription, type(desc), len(desc)))
    except IndexError:
        return False

    feeditem = Item(
            feedid = int(feedid),  # int
            title = title,  # str
            link = link,  # str
        # description = desc.encode(),  # bytes
        description = desc,
    )

    # followed is optional :
    # StrField에 대해, 없거나 빈 문자열이면 len(<object>) -> 0
    # StrField에 대해, 없으면 not(<object>) -> True
    def _add(item, fieldname: str, field: str, parse = True, usingCDATA = True):
        logger.debug("-*|{fieldname} : ({len}){field}"
                     .format_map({'fieldname': fieldname, 'len': len(field), 'field': field}))
        if field and (len(field) > 0):
            logger.debug("-*|{fieldname} not Null(None|zero length)".format_map({'fieldname': fieldname}))
            if parse:
                value = page.select(field)[0].get_text()
            else:
                value = field

            # print(fieldname,len(value),sep=':')
            if usingCDATA:
                setattr(item, fieldname, make_CDATA(value))
            else:
                setattr(item, fieldname, value)

            return True
        return False

    _add(feeditem, "author", rset.itemauthor)
    _add(feeditem, "category", rset.itemcategory)
    # guid = page.select(rset.itemguid)[0].get_text()

    if not (rset.itemguidtype) or len(rset.itemguidtype) == 0:
        logger.debug("*- guid is not setted.")
        guidtype = None
    else:
        guidtype = str(rset.itemguidtype)

    if guidtype == "find":
        _add(feeditem, "guid", rset.itemguid, parse = True, usingCDATA = False)
    elif guidtype == "regular":
        if rset.itemguidfrom == "item":
            guid = regsub(iter, *str(rset.itemguid).split("\\!\\"))
        elif rset.itemguidfrom == "list":
            guid = regsub(Ruleset.return_item(feedid).listurl, *rset.itemguid.split("\\!\\"))
        else:
            guid = None
        _add(feeditem, "guid", guid, parse = False, usingCDATA = True)
    else:  # guidtype = None
        pass

    # comment = make_CDATA(rset.itemcomment)
    # _add(i, "comment", rset.itemcomment, parse = False, usingCDATA = True)
    # if
    if not (not (rset.itempub_date)) and len(rset.itempub_date) > 0:
        # 웹 서비스상에서 날짜 형식 지정시 예시를 표현해주도록 할 것
        _rawtime = page.select(str(rset.itempub_date))[0].get_text().encode().strip()
        _length = datetime.now().strftime(str(rset.itempub_date_format)).encode()
        _converted = datetime.strptime((_rawtime[0:len(_length)] + b" +0900").decode(),
                                       str(rset.itempub_date_format) + ' %z')
        pub_date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', _converted.utctimetuple())
        _add(feeditem, "pub_date", pub_date, parse = False, usingCDATA = False)

    return feeditem
