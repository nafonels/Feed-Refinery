#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from datetime import datetime

from crawler import http_opener, page_parser

__version__ = "$"

"""
TODO:
1. cookie를 지원할 수 있도록 할 것.
2. sample인 hufs.ac.kr에서 favicon설정이 되어있지 않았음.
"""


def makeRSS(feedurl, title = str(), desc = str(), category = str(), list = str(),
            searchitems = str(), image = None, encoding = None):
    """
    param:
        feedurl = rss를 생성할 목록 url
        title = rss의 이름
        desc = rss 설명
        category = rss의 분류(선택)
        list = 목록에서 추출될 각 item의 css selector
        item = 각 searchitemsitem에서 desc로 추출될 내용의 css selector

    rss가 제공되지 않는 게시판에서 다음을 수행하도록 한다.
    1. 게시판의 목록을 통해 item을 추출한다.
    2. 각 item에서 선택된 부분만을 추출해서 본문을 만든다.
    3. 작성된 데이터를 토대로 rss xml을 만든다.(rss 2.0)
    만들어진 xml raw Data를 string으로 return한다.
    """
    # a = getpage(feedurl)
    # if title == "":
    #    title = a.getTitle()
    # 
    # 
    # 
    # Agent가 rss를 publish한 시각. publishing cache를 갱신한 시각이다.
    # pub_date = time.strftime(u'%a, %d %b %Y, %H:%M:%S GMT',time.gmtime())
    #
    #   
    # <channel>
    #         <title></title>
    #         <link></link>
    #         <description></description>
    #         <!-- opitonal -->
    #         <pubDate></pubDate>
    #         <lastBuildDate></lastBuildDate>
    #         <category><!-- for catalog system --></category>
    #         <image>
    #             <url></url>
    #             <title></title>
    #         </image>

    feed = rssfeed(
            link = feedurl,
            title = title,
            description = desc,
            category = category,
            searchitems = searchitems,
            encoding = encoding
    )

    if image is not None:
        feed.setImage(image)

    # <link href="파비콘 이미지 경로” rel="shortcut icon"/> 
    # for iter in itemlist:
    #   
    #   feed.addItem(title,
    #                link,
    #                desc,
    #                author,
    #                category,
    #                comment,
    #                guid,
    #                isperma,
    #                pub_date,
    #                )
    # 
    # if feed is changed:
    #   
    # 
    # item/feed 변경을 확인한 시각.
    # lastBuild = time.strftime(u'%a, %d %b %Y, %H:%M:%S',time.gmtime())

    # feed['descipiton'] = "test"
    # print (feed.__dict__)
    # print (feed.items())
    # print (rssfeed.type)
    # feed.prettyPrint()
    # update(feed)
    # print (feed.items())
    return feed


class rssfeed(dict):
    """
    내부 데이터 타입 : dict()
    """

    def __init__(self,
                 link,
                 title,
                 searchitems,
                 encoding = 'utf-8',
                 **kwargs
                 ):
        # super(rssfeed, self).__init__()
        self.info = dict()
        self.config = dict()
        self.info['encoding'] = encoding
        self.info['version'] = "2.0"
        self.config['link'] = link
        self.config['searchitems'] = searchitems
        # 기타(접속정보)

        self.feeditems = 'None'

        # self.info = kwargs
        self['title'] = title
        self['link'] = link
        self['generator'] = "customrssserver"
        self.update(kwargs)

        # print (self.info)

    def setImage(self, url):
        link = self['link']
        title = self['title']
        self['image'] = {'link': link, 'title': title, 'url': url}

    # def print(self):
    #     print (self)

    def setItemPropertise(self, *kwds, **kwargs):
        self.feeditems = FeedItems(**kwargs)
        pass

    # def __str__(self):
    #     pass

    def __makeXmlList__(self):
        # ret = list()
        header = """<?xml version="1.0" encoding="%s"?>
<rss version="%s"
\txmlns:dc="http://purl.org/dc/elements/1.1"
\txmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
\txmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
\txmlns:content="http://purl.org/rss/1.0/modules/content/"
>""" % (self.info['encoding'], self.info['version'])

        ret = header.splitlines()

        def makeElement(target, level = 1):
            ret = list()
            # res = str()
            for e, c in target.items():
                if isinstance(c, dict):
                    """image element등 하위 element를 가지고 있는 경우를 위함"""
                    ret.append("\t" * level + "<%s>" % e)
                    # ret.expand(makeElement(c))
                    ret.extend(makeElement(c))
                    ret.append("\t" * level + "</%s>" % e)
                    continue
                # else:
                a = "\t" * level + "<{0}>{1}</{0}>".format(e, c)
                ret.append(a)

            return ret

        ret.append("\t<channel>")
        ret.extend(makeElement(self, 2))

        for item in self.feeditems:
            ret.append("\t\t<item>")
            ret.extend(makeElement(item, 3))
            ret.append("\t\t</item>")

        ret.append("\t</channel>")
        ret.append("</rss>")

        return ret

    def toxml(self, encoding = 'utf8'):
        return self.toprettyxml()

    def toprettyxml(self, indent = "", newl = "", encoding = ""):
        return newl.join(self.__makeXmlList__()).replace('\t', indent).encode()

    def changeChannelInfo(self, info = dict()):
        self.info.update(info)


class FeedItems(list):
    def __init__(self,
                 title = str(),
                 # link = None,
                 desc = str(),
                 author = str(),
                 category = str(),
                 # comments = None,
                 # guid = "items",
                 pub_date: str = str(),
                 pub_date_format: str = str(),
                 encoding = None):

        self.config = dict()
        self.info = dict()

        self.config['title'] = title
        # self.config['link'] = link
        self.config['description'] = desc
        self.config['author'] = author
        self.config['category'] = category
        # self.config['comments'] = comment
        # self.config['guid'] = guid
        self.config['pub_date'] = pub_date
        self.config['pub_date_format'] = pub_date_format

        self.info['encoding'] = encoding

        self.linklist = list()

    def update(self, itemlist = list(), renew = False):
        if (self.linklist == itemlist) and not renew:
            return False

        # print (itemlist)
        items = list()

        for iter in itemlist:
            item = dict()

            # item['link'] = item['guid'] = quote(iter)
            item['link'] = item['guid'] = ''.join(["<![CDATA[", iter, "]]>"])
            con = http_opener.openPage(iter)
            page = page_parser.parse(con, encoding = self.info['encoding'])

            # base = con.info.getheader('Date'),
            # print (base)

            # t =  page.select(feed.config['searchitems'])

            for key, iter in self.config.items():  # not in 'link', 'guid'
                if key.find('Format') != -1:  # pub_date_format
                    continue

                val = page.select(iter)[0]

                if key.find('desc') != -1:  # desc
                    # print(val.prettify(formatter="html"))
                    item[key] = ''.join(["<![CDATA[", val.prettify(formatter = "minimal"), "]]>"])

                elif key.find('pub_date') == -1:  # other
                    item[key] = "<![CDATA[" + val.get_text() + "]]>"

                else:  # pub_date
                    rawtime = val.getText().encode('utf8')
                    length = datetime.now().strftime(self.config['pub_date_format'])
                    time1 = datetime.strptime(
                            (rawtime[0:len(length)] + b" +0900").decode(),
                        self.config['pub_date_format'] + ' %z')

                    # print("1",time1.utctimetuple())
                    # print("2", item[key])
                    # print(type(time1), type(time1.utctimetuple()))
                    # print("=", time.strftime("%a, %d %b %Y, %H:%M:%S", time1.utctimetuple()))

                    item[key] = time.strftime("%a, %d %b %Y, %H:%M:%S", time1.utctimetuple())

            items.append(item)

        self[:] = items
        # print(self.config)
        # print(len(self))

        self.linklist = itemlist
        return True


def update(feed):
    """
    이미 등록된 feed에 대하여 다음을 수행한다.
    1. feed에 대하여 data를 재생성한다.

    # page에 대한 connection 생성
    # 생성된 connection에 대해 cookie 획득
    # page parse하여 list 획득
    # list따라 page pare하여 feeditem 획득

    """
    # 서버 배포 갱신 시간 - 인스턴스 갱신 메소드 실행시 자동 변경, 여기서 넣지 말 것.

    # 아직 회원 인증 로그인은 제공하지 않음
    http_opener.makeOpenerWithCookie(feed.config['link'], {})

    listpage = page_parser.parse(http_opener.openPage(feed.config['link']))
    t = listpage.select(feed.config['searchitems'])

    itemlist = [http_opener.make_absolute_uri(feed.config['link'], iter.find('a').attrs['href'])
                for iter in t]
    # print (itemlist)

    feed.feeditems.info['encoding'] = listpage.original_encoding

    param = [itemlist]
    if not 'lastBuildDate' in feed.info: param.append(True)
    if feedupdate(feed.feeditems, param):
        feed.info['lastBuildDate'] = time.strftime('%a, %d %b %Y, %H:%M:%S', time.gmtime())

    feed.info['pub_date'] = time.strftime('%a, %d %b %Y, %H:%M:%S', time.gmtime()),

    pass


def feedupdate(feedItems, param):
    feedItems.update(*param)