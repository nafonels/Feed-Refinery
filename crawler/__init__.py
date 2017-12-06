#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crawler.feed_updater import update
from model import db_session
from model.buildinfo import BuildInfo
from model.ruleset import Ruleset
from util.logger import logger

__version__ = "$"


def updateAll():
    # todo: 첫 갱신 후 ruleset에 기록된 시간간격대로 feed를 갱신하도록 함
    """
    1. Ruleset과 BuildInfo 동기화
    2. Ruleset의 항목대로 Item update
    3.

    """
    # update each rss
    rules = Ruleset.query.all()

    # todo: update로 옮기고, 그냥 전체 loop만 돌 것
    for rule in rules:
        _validate_buildinfo(rule.id)
        update(rule.id)

    return True


    # apscheduler


def _validate_buildinfo(feedid):
    # todo: 후에 ruleset에서 각각 따로 지정할 수 있도록 할 것
    _defaultInterval = 10  # minute

    buildinfo = BuildInfo.return_item(feedid)
    if not buildinfo or type(buildinfo) is not BuildInfo:
        logger.debug("*- initial feed update : {}".format(feedid))
        buildinfo = BuildInfo(id = feedid,
                              check_interval = _defaultInterval)
        db_session.add(buildinfo)
        db_session.commit()
    return buildinfo
