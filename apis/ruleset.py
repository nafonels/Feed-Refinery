
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Resource, abort, reqparse

from model import db_session
from model.ruleset import Ruleset as model_Ruleset

__version__ = "$Revision$"
ruleset_parser = reqparse.RequestParser()

ruleset_parser.add_argument('listurl', type = str)
ruleset_parser.add_argument('encoding', type = str)
ruleset_parser.add_argument('title', type = str)
ruleset_parser.add_argument('description', type = str)
ruleset_parser.add_argument('category', type = str)
ruleset_parser.add_argument('itemlink', type = str)
ruleset_parser.add_argument('nextpagelink', type = str)
ruleset_parser.add_argument('maxcheckpage', type = str)
ruleset_parser.add_argument('itemtitle', type = str)
ruleset_parser.add_argument('itemauthor', type = str)
ruleset_parser.add_argument('itemcategory', type = str)
ruleset_parser.add_argument('itemdesc', type = str)
ruleset_parser.add_argument('itemguidtype', type = str)
ruleset_parser.add_argument('itemguidfrom', type = str)
ruleset_parser.add_argument('itemguid', type = str)
ruleset_parser.add_argument('iteupub_date', type = str)
ruleset_parser.add_argument('itempub_date_format', type = str)


class Rulesets(Resource):
    def get(self):
        results = []
        for row in Ruleset.query.all():
            results.append(row.make_ret())
        return results

    def post(self):
        try:
            args = ruleset_parser.parse_args()
            feed_id = model_Ruleset.query.count() + 1
            feed = model_Ruleset(
                    listUrl = args['listUrl'],
                    encoding = args['encoding'],
                    title = args['title'],
                    description = args['description'],
                    category = args['category'],
                    itemlink = args['itemlink'],
                    nextpagelink = args['nextpagelink'],
                    maxcheckpage = args['maxcheckpage'],
                    itemtitle = args['itemtitle'],
                    itemauthor = args['itemauthor'],
                    itemguidtype = args['itemguidtype'],
                    itemguidfrom = args['itemguidfrom'],
                    itemguid = args['item'],
                itempub_date = args['itempub_date'],
                itempub_date_format = args['itempub_date_format']
                )
            db_session.add(feed)
            db_session.commit()
        except:
            abort(500)
        return feed_id, 201
        pass

    def delete(self):
        pass

    def put(self):
        #  for entirely change
        # collection : not accepted method
        pass

    def patch(self):
        # for partialy change
        # collection : not accepted method
        pass


class Ruleset(Resource):
    def get(self, rule_id):
        row = Ruleset.query.filter(Ruleset.id == rule_id).first()
        if row is None:
            abort(404)
        return row

    def delete(self):
        pass

    def put(self, rule_id):
        pass

    def patch(self, rule_id):
        # for partialy change
        # collection : not accepted method
        row = Ruleset.query.filter(Ruleset.id == rule_id).first()
        args = ruleset_parser.parse_args()
        return 200
        pass
