from flask.views import View, MethodView
from ortelius.models.Fact import Fact
from flask import request, abort, jsonify, render_template_string

'''
    Get facts with optional search params.
    ?from=12-22-1560 - search facts from this date
    ?to=03-30-1570 - search facts to this date

    ?topleft - coordinates of top left corner of the screen
    ?bottomright - coordinates bottom right corner of the screen

    ?search - determinate search
    ?search&name  - search by name
    ?search&date - search by date (use end date)

    Ex.:
    http://handymap.com/api/facts/36 - one fact by id
    http://handymap.com/api/facts?from=12-22-1560&to=03-30-1570&topleft=65.45,56.89&bottomright=69.45,50.89 - facts by dates in given quadrant
'''


class FactsView(MethodView):
    def get(self, id=None):
        query = Fact.query
        if id is None:
            get_params = request.args.to_dict()
            if get_aprams:
                if 'topleft' and 'bottomright' in query.keys():
                    pass
                if 'from' in query.keys():
                    query = query.filter(Fact.start_date_year <= get_params['from'])
                if 'to' in query.keys():
                    query = query.filter(Fact.start_date_year >= get_params['to'])
                facts = query.all()
                raise
            else:
                facts = query.all()
            return jsonify(get_params)
        else:
            return query.get(id)

    def post(self):
        raise NotImplementedError()

    def put(self, id):
        raise NotImplementedError()

    def delete(self, id):
        raise NotImplementedError()
