# -*- coding: utf-8 -*-
import logging

from flask import Flask
from flask_restful import Api
from flask_restful import Resource

import crawler
from apis.ruleset import Ruleset, Rulesets
from util.logger import logger
from webview.views import my_view

app = Flask(__name__)
api = Api(app)

app.register_blueprint(my_view)

# apis
class Category(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass

    def patch(self):
        pass


api.add_resource(Rulesets, '/apis/v0.1/rulesets')
api.add_resource(Ruleset, '/apis/v0.1/rulesets/<rule_id>')
api.add_resource(Category, '/apis/v0.1/categories')


@app.teardown_request
def shutdown_session(exception = None):
    model.db_session.remove()


def crowl_all():
    logger.info('startup crwaling.')
    crawler.updateAll()


def rss_renew():
    minute = 10
    """
    1. 첫 실행시 먼저 rss를 갱신한다.
    2. 1분마다 각각의 id-loop dict를 순회하며 loop를 늘린다.
    3. if loop[feedid] >= Interval.checkinterval(feedid=feedid):
            makeRSS.update(feedid)
    """
    # timetable = makeRSS.newTimeTable()
    while True:
        _renew()
        # for feedid, loop in iter(timetable.items()):
        # 	loop = loop + 1
        # 	if loop >= makeRSS.Interval(feedid=feedid).checkinterval:
        # 		makeRSS.update(feedid)
        # 		loop = 0
        # 	timetable[feedid] = loop
        # makeRSS.check()
        import time
        time.sleep(minute * 60)
# todo: refactoring functions about make rss
# fixme: not connected appropriate module
def _renew():
    crawler.updateAll()
    logger.info("All feeds are updated.")


def _renewprocess():
    # rss_renew()
    # rssRenewThread = threading.Thread(target=rss_renew)
    # rssRenewThread.daemon = True
    # rssRenewThread.start()
    from multiprocessing import Process
    # flag를 보고 stop할 수 있도록 해야 함
    rss_renew_process = Process(target = rss_renew)
    rss_renew_process.start()

    # httpThread = threading.Thread(target = httpd.serve_forever)
    # httpThread.daemon = False # 다른 쓰레드에 종속적?
    # httpThread.start()
    httpd.serve_forever()


if __name__ == '__main__':
    import model
    from crawler.scheduler import scheduler

    a = logging.getLogger('default_logger')
    a.debug('testlog')
    b = logging.getLogger()
    b.debug('testb')
    model.init_db()
    scheduler.start()
    crowl_all()
    app.run(debug = True, host = "0.0.0.0")

