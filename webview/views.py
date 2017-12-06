# !/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, redirect, render_template, request, url_for

from crawler import rss_builder
from model import db_session
from model.ruleset import Ruleset
from util.logger import logger

__version__ = "$Revision$"

my_view = Blueprint('my_view', __name__)


# todo: feeditem을 확인할 수 있는 페이지를 생성할 것
# todo: RSS를 받아올 수 있는 링크들이 모여있는 페이지를 생성할 것
# todo: ATOM을 생성할 수 있도록 할 것

@my_view.route('/')
def index():
    logger.debug("indexTest")
    return render_template('index.html')


@my_view.route('/ruleset_list')
def list_ruleset():
    rows = Ruleset.return_list_of_every_item()
    return render_template('list_ruleset.html', entries = rows)


@my_view.route('/new_ruleset')
def new_feed_page():
    return render_template('ruleset.html')
    pass


@my_view.route('/add_ruleset', methods = ['POST'])
def add_ruleset():
    # TODO : add시 flash 메시지를 띄우도록 할 것
    # TODO : 이를 위해서는 flash를 위해 세션을 생성할 필요가 있다.

    # if not session.get('session_id'):
    #   abort(401)
    logger.debug(request.form)
    ruleset = Ruleset()

    set_field(ruleset)

    db_session.add(ruleset)
    db_session.commit()

    return redirect(url_for('my_view.list_ruleset'))  # str(request.form) + "\n is checked"


def set_field(ruleset):
    ruleset.listUrl = request.form['listUrl']
    ruleset.encoding = request.form['encoding']
    ruleset.title = request.form['title']
    ruleset.description = request.form['description']
    ruleset.category = request.form['category']
    ruleset.itemlink = request.form['itemlink']
    ruleset.nextpagelink = request.form['nextpagelink']
    ruleset.maxcheckpage = request.form['maxcheckpage']
    ruleset.itemtitle = request.form['itemtitle']
    ruleset.itemauthor = request.form['itemauthor']
    ruleset.itemcategory = request.form['itemcategory']
    ruleset.itemdescription = request.form['itemdescription']
    ruleset.itemguidtype = request.form['itemguidtype']
    ruleset.itemguidfrom = request.form['itemguidfrom']
    ruleset.itemguid = request.form['itemguid']
    ruleset.itempub_date = request.form['itempub_date']
    ruleset.itempub_date_format = request.form['itempub_date_format']


@my_view.route('/change_ruleset/<rule_id>')
def change_feed_page(rule_id):
    ruleset = Ruleset.return_item(rule_id)

    return render_template('ruleset.html', entry = ruleset)


@my_view.route('/modify_ruleset', methods = ['POST'])
def modify_ruleset():
    # TODO : modify시 flash 메시지를 띄우도록 할 것
    # TODO : 이를 위해서는 flash를 위해 세션을 생성할 필요가 있다.

    # if not session.get('session_id'):
    #   abort(401)
    logger.debug(request.form)

    rule_id = request.form['id']

    ruleset = Ruleset.return_item(rule_id)
    set_field(ruleset)

    db_session.commit()
    return redirect(url_for('my_view.list_ruleset'))  # str(request.form) + "\n is checked"


@my_view.route('/rss/rule/<rule_id>')
def provide_rss_rule(rule_id):
    return rss_builder.generate_rss(rule_id)
