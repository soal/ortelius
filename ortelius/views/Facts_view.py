# import time

import datetime
from json import dumps
from flask import request, abort, jsonify
from ortelius.middleware import serialize, convert_wikitext
from flask.views import MethodView

from ortelius.types.historical_date import HistoricalDate as hd, DateError
from ortelius.models.Date import Date
from ortelius.models.Fact import Fact
from ortelius.models.Coordinates import Quadrant, Shape, Coordinates

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

def filter_by_time(query, args):
    try:
        start = hd(args['from'])
    except KeyError:
        start = hd(-50000101)
    try:
        end = hd(args['to'])
    except KeyError:
        end = hd(datetime.datetime.now())

    query = query.filter(Fact.start_date.has(Date.date >= start.to_int()),
                         Fact.end_date.has(Date.date <= end.to_int())
                        )
    return query

def filter_by_geo(query, args):
    try:
        top_left = [float(x) for x in args['topleft'].split(',')]
        bottom_right = [float(x) for x in args['bottomright'].split(',')]
    except KeyError:
        return query
    # CYCLE_START = time.clock()
    quadrants_coordinates = []
    for c in Quadrant.quadrants:
        if c[0] >= top_left[0] - 4 and c[0] <= bottom_right[0] and c[1] >= top_left[1]-4 and c[1] <= bottom_right[1]:
            quadrants_coordinates.append(','.join([str(c[0]), str(c[1])]))

    # CYCLE_END = time.clock()
    # print('CYCLE: ', CYCLE_END - CYCLE_START)
    # GENERATOR_START = time.clock()
    # quadrants_coordinates = [y for y in filter(lambda x: x[0] >= top_left[0]-4 and x[0] <= bottom_right[0], Quadrant.quadrants)]
    # quadrants_coordinates = [ ','.join([str(z) for z in y]) for y in filter(lambda x: x[1] >= top_left[1]-4 and x[1] <= bottom_right[1], quadrants_coordinates)]
    # GENERATOR_END = time.clock()
    # print('GENERATOR: ', GENERATOR_END - GENERATOR_START)


    query = query.filter(Fact.shape.has(Shape.coordinates.any(Coordinates.quadrant_hash.in_(quadrants_coordinates))))

    return query

def filter_by_weight(query, args):
    try:
        weight = args['weight']
    except KeyError:
        return query

    query = query.filter(Fact.weight <= weight)
    return query


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

    def get(self, id=None):
        if id:
            res = jsonify(self.one(id))
            return res
        else:
            args = request.args.to_dict()
            if args:
                query = Fact.query
                # TIME_START = time.clock()
                try:
                    query = filter_by_time(query, args)
                except DateError as e:
                    response = jsonify(e.api_error(400))
                    response.status_code = 400
                    return response
                # TIME_END = time.clock()
                # print("TIME: ", TIME_END - TIME_START)
                # GEO_START = time.clock()
                query = filter_by_geo(query, args)
                query = filter_by_weight(query, args)
                # GEO_END = time.clock()
                # print("GEO: ", GEO_END - GEO_START)

                # DB_START = time.clock()
                result = query.all()
                # DB_END = time.clock()
                # print("DB: ", DB_END - DB_START)
                serialized_result = []

                for fact in result:
                    serialized = serialize(fact)
                    serialized['start_date'] = fact.start_date.date.to_string()
                    serialized['end_date'] = fact.end_date.date.to_string()
                    serialized['type'] = { 'name': fact.type.name, 'label': fact.type.label }
                    serialized['shape'] = serialized['shape_id']
                    serialized['description'] = serialized['description']
                    serialized.pop('start_date_id')
                    serialized.pop('end_date_id')
                    serialized.pop('shape_id')
                    serialized.pop('type_name')
                    serialized.pop('text')
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
