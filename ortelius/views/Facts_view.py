from json import dumps
from flask import request, abort, jsonify, render_template_string
from ortelius.middleware import serialize, convert_wikitext
from flask.views import MethodView

from ortelius.types.historical_date import HistoricalDate as hd, DateError
from ortelius.models.Date import Date
from ortelius.models.Fact import Fact

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

acceptable_params = {'from': 'start_date',
                     'to': 'end_date',
                     'topleft': None,
                     'bottomright': None,
                     'search': None,
                     'name': 'name'}


class FactsView(MethodView):
    """Facts view"""
    
    def one(self, id):
        fact = Fact.query.get_or_404(id)
        result = serialize(Fact.query.get(id))

        result['start_date'] = fact.start_date.date.to_string()
        result['end_date'] = fact.end_date.date.to_string()
        result['type'] = { 'name': fact.type.name, 'label': fact.type.label }
        result['shape'] = result['shape_id']
        # result['description'] = convert_wikitext(result['description'])
        # result['text'] = convert_wikitext(result['text'])
        # result.pop('text')
        result.pop('start_date_id')
        result.pop('end_date_id')
        result.pop('shape_id')
        result.pop('type_name')
        return result

    def filtered_by_time(self, query, request):
        try:
            start = hd(request.args.to_dict()['from'])
        except KeyError:
            start = None
        try:
            end = hd(request.args.to_dict()['to'])
        except KeyError:
            end = None

        query = query.filter(Fact.start_date.has(Date.date >= start.to_int()),
                             Fact.end_date.has(Date.date <= end.to_int())
                            )
        return query

    def get(self, id=None):
        if id:
            res = jsonify(self.one(id))
            return res
        else:
            if request.args.to_dict():
                query = Fact.query
                try:
                    query = self.filtered_by_time(query, request)
                except DateError as e:
                    response = jsonify(e.api_error(400))
                    response.status_code = 400
                    return response
                result = query.all()
                serialized_result = []

                for fact in result:
                    serialized = serialize(fact)
                    serialized['start_date'] = fact.start_date.date.to_string()
                    serialized['end_date'] = fact.end_date.date.to_string()
                    serialized['type'] = { 'name': fact.type.name, 'label': fact.type.label }
                    serialized['shape'] = serialized['shape_id']
                    serialized['description'] = convert_wikitext(serialized['description'])
                    serialized.pop('start_date_id')
                    serialized.pop('end_date_id')
                    serialized.pop('shape_id')
                    serialized.pop('type_name')
                    # serialized.pop('text')
                    serialized_result.append(serialized)

                return dumps(serialized_result)
            else:
                abort(501)



    def post(self):
        raise NotImplementedError()

    def put(self, id):
        raise NotImplementedError()

    def delete(self, id):
        raise NotImplementedError()

class TextView(MethodView):
    def get(self, id=None):
        if id:
            fact = Fact.query.get_or_404(id)
            return convert_wikitext(fact.text)
        else:
            abort(404)
