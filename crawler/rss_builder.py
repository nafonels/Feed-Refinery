#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from crawler.util import make_CDATA
from model import db_session
from model.buildinfo import BuildInfo
from model.feed import Feed
from model.item import Item
from model.ruleset import Ruleset
from util.logger import logger

# import model

__version__ = "$"

info = {'version': "2.0", "generator": "Feed-Refinary 0.4"}


def generate_rss(rule_id):
    # 이미 생성된 feed item을 이용해 실제 rss를 생성
    """
    1. if exist(RSS(id=rule_id)) and (BuildInfo(rule_id).pub_date == RSS(id=Feedid).pub_date):
            return RSS(id=rule_id).rss.encode()
    2. else:
            return makeRSSCache(rule_id).encode()

    """
    # cursor = sql_obj.sqlite_select_data('RSS', ['*'], 'id = %s' % rule_id)
    # rss = cursor.fetchone()
    # ->
    rss = Feed.return_item(rule_id)
    buildinfo = BuildInfo.return_item(rule_id)

    # _ipd = 4
    # _rpd = 2
    # _rr = 1

    # if (len(rss) != 0) and (BuildInfo[_ipd] == rss[_rpd]):
    if rss and (str(buildinfo.pub_date) == str(rss.pub_date)):
        logger.info("*- rss cached")
        # return rss[_rr].encode()
        return bytes(rss.rss)

    # else:
    # 	return makeRSSCache(rule_id).encode()

    items = Item.return_item(rule_id)
    items = Item.query.filter(Item.feedid == rule_id).all()
    # feedid에 해당하는 item이 없는 경우
    if not items or len(items) == 0:
        # todo: feed가 없을때는 feed를 생성하도록 할 것.
        return "this feed is not ready to service. please wait for moment.".encode()

    def itemsort(x):
        # _pub_date = 8
        ret = time.strptime(str(x.pub_date), '%a, %d %b %Y %H:%M:%S GMT')
        # return x[_pub_date]
        return ret

    if items[0].pub_date and len(items[0].pub_date) > 0: items.sort(key = itemsort, reverse = True)

    # cursor = sql_obj.sqlite_select_data('Ruleset',['*'], 'rule_id = %s' % rule_id)
    # rule = cursor.fetchone()
    rule = Ruleset.return_item(rule_id)

    ret = _genrss(rule, items, buildinfo)

    if not rss:
        logger.debug("*- insert New RSS")
        rss = Feed(id = rule_id,
                   rss = ret,
                   pub_date = str(BuildInfo.pub_date)
                   )
        # sql_obj.sqlite_insert_data("RSS", [rule_id, ret, BuildInfo.pub_date])
        db_session.add(rss)
    else:
        logger.debug("*- update existed RSS")
        rss.rss = ret
        rss.pub_date = str(BuildInfo.pub_date)
    # sql_obj.sqlite_update_data("RSS", {"rss":ret,
    # "pub_date":BuildInfo.pub_date}, "id = %s" % rule_id)
    db_session.commit()
    # rss._sqlobj.cursor.close()

    # return type:bytes
    return ret


# 	testrss = """<?xml version="1.0" encoding="UTF-8"?>
# <rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">
# 	<channel>
# 		<title> %s </title>
# 	</channel>
# </rss>""" % feedid
# 	return testrss.encode()
def _genrss(rule, items, BuildInfo):
    def makeElement(target, level = 1):
        ret = list()
        # res = str()
        for e, c in target.items():
            if isinstance(c, dict):
                """image element등 하위 element를 가지고 있는 경우를 위함"""
                ret.append("\t" * level + "<%s>" % e)
                ret.extend(makeElement(c, level + 1))
                ret.append("\t" * level + "</%s>" % e)
                continue
            # else:
            if not (not (c)) or len(str(c)) > 0:
                a = "\t" * level + "<{0}>{1}</{0}>".format(e, c)
                ret.append(a)

        return ret

    header = """<?xml version="1.0" encoding="%s"?>
<rss version="%s"
\txmlns:dc="http://purl.org/dc/elements/1.1"
\txmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
\txmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
\txmlns:content="http://purl.org/rss/1.0/modules/content/"
>""" % ("UTF-8", info['version'])

    ret = header.splitlines()
    ret.append('\t<channel>')

    listurl = str(rule.listUrl)
    if listurl.count('&'):
        listurl = make_CDATA(listurl)

    # Required : title, link, desc
    feedinfo = {"title":         rule.title,
                "link":          listurl,
                "description":   rule.description,
                "category":      rule.category,
                "pub_date":      BuildInfo.pub_date,
                "lastBuildDate": BuildInfo.last_builddate,
                "generator": info['generator']
                }

    # if not (not (rule.image)) and len(rule.image) > 0:
    #     feedinfo.update({"image": {
    #         # "url":         rule.image,
    #         "title":       rule.title,
    #         "link":        rule.listurl,
    #         "description": rule.desc,
    #         "width":       rule.imagewidth,
    #         "height":      rule.imageheight
    #     }})

    ret.extend(makeElement(feedinfo, 2))

    # Required : title, link, description
    for item in items:
        iteminfo = {"title":       item.title,
                    "link":        item.link,
                    "description": item.description,
                    "author":      item.author,
                    "category":    item.category,
                    "comments":    item.comment,
                    "guid":        item.guid,
                    "pub_date":    item.pub_date
                    }
        ret.append('\t\t<item>')
        ret.extend(makeElement(iteminfo, 3))
        ret.append('\t\t</item>')

    ret.append('\t</channel>')
    ret.append('</rss>')

    ret = "\n".join(ret)
    return ret.encode()


def makeRSSCache(feedid):
    return str(feedid)
