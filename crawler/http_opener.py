#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import error, request
from urllib.parse import urlencode, urljoin

from crawler.utils.responsed_string import responsedString
from util.logger import logger

__version__ = "$"

global opener


def makeOpenerWithCookie(url, value = dict(), headers = dict()):
    """
    todo:
    1. default protocol : http 설정

    """
    # cj = CookieJar()

    makeOpenerWithoutCookie(url)
    global opener

    if value is not None:
        data = urlencode(value).encode('utf8')
    else:
        data = None
    req = request.Request(url, data, headers, origin_req_host = None)
    try:
        res = opener.open(req)
    except error.HTTPError:  # , e:
        raise  # e
    except error.URLError:  # , e:
        raise  # e
    # except socket.gaierror:
    #     """주소가 맞지 않거나, 인터넷에 연결되지 않은 경우"""
    #    raise
    finally:
        pass
        # logger.debug("responsed w/t cookie. cookiejar: {}".format(cookie.cookiejar))
    if "Set-Cookie" in res.headers:
        """쿠키를 받아온 경우. 로그인 성공 또는 추적용"""
        return True
    else:
        """cookie가 없는 경우, login page가 아니거나 login 실패"""
        return False


def makeOpenerWithoutCookie(url: object) -> object:
    # todo: default protocol : http 설정
    # cj = CookieJar()
    cookie = request.HTTPCookieProcessor()
    global opener
    opener = request.build_opener(cookie)
    request.install_opener(opener)

    return True


# parameter : html document's url <- "string"
# return : all image's url -> list["string", ...]

# class getPage(object):
#     """
#     이제 opener를 사용해서 실제로 page를 받아온다.

#     실제로는 login과 관련해서 login url을 받아 cookie를 받아오는 부분을 처리해야 하고, 
#         이후 cookie를 이용해 실제 page를 받은 후 인증정보와 함께 download처리를 할 수 있어야 함.
#     """
#     def __init__(self):
#         self.address = str()
#         self.referer = str()
#         pass

#     def openpage(self, address, referer=""):
#         self.address = address
#         self.referer = referer
#         self.opener = None
#         self._openpage()

#     def _openpage(self):
#         req = request.Request(self.address)
#         if len(self.referer):
#             req.add_header("Referer", self.referer)

#         try:
#             res = request.urlopen(req)
#         except Exception, e:
#             raise e
#         finally:
#             pass

#     def download(self):
#         pass


def openPage(url, query = dict(), headers = dict()) -> responsedString:
    global opener

    if len(query) == 0:
        query = None
    else:
        query = urlencode(query)

    req = request.Request(url, query, headers, origin_req_host = None)

    res = None
    count = 0
    while count < 3:
        import socket
        try:
            res = opener.open(req)
        except error.URLError:
            count = count + 1
            logger.info("-* failed connect to : {}. retrying {} / 3".format((url, count)))
            continue
        except socket.error:
            count = count + 1
            continue
        except:
            raise ConnectionError
        else:
            break
    if not res: raise ConnectionError
    ret = responsedString(res)

    logger.debug("page opened. returned {} length. Info : {}".format((len(ret)), res.info()))
    return ret


# __supertype = str


def make_absolute_uri(*kwds, **kwargs):
    return urljoin(*kwds, **kwargs)