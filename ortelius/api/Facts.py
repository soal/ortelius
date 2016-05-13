import hug
import datetime

from ortelius.database import db
from ortelius.models.Date import Date
from ortelius.models.Fact import Fact
from ortelius.models.Coordinates import Quadrant, Shape, Coordinates
from ortelius.types.historical_date import DateError, HistoricalDate as hd
from ortelius.middleware import serialize, make_api_response

'''
    Get facts with optional search params.
    ?start_date=12-22-1560 - search facts from this date
    ?end_date=03-30-1570 - search facts to this date

    ?topleft - coordinates of top left corner of the screen
    ?bottomright - coordinates bottom right corner of the screen

    ?search - determinate search
    ?search&name  - search by name
    ?search&date - search by date (use end date)

    Ex.:
    http://handymap.com/api/facts/36 - one fact by id
    http://handymap.com/api/facts?start_date=12-22-1560&end_date=03-30-1570&topleft=65.45,56.89&bottomright=69.45,50.89 - facts by dates in given quadrant
'''

def filter_by_time(query, start_date, end_date):
    '''Filter facts by date'''
    if start_date:
        start = hd(start_date)
    else:
        start = hd(-50000101)
    if end_date:
        end = hd(end_date)
    else:
        end = hd(datetime.datetime.now())
    query = query.filter(Fact.start_date.has(Date.date >= start.to_int()),
                         Fact.end_date.has(Date.date <= end.to_int())
                        )
    return query


def filter_by_geo(query, topleft, bottomright):
    '''Filter facts by given quadrants in geocoordinates'''
    if topleft and bottomright:
        top_left = [float(x) for x in topleft]
        bottom_right = [float(x) for x in bottomright]
    else:
        return query
    quadrants_coordinates = []
    for c in Quadrant.quadrants:
        if c[0] >= top_left[0] - 4 and c[0] <= bottom_right[0] and c[1] >= top_left[1]-4 and c[1] <= bottom_right[1]:
            quadrants_coordinates.append(','.join([str(c[0]), str(c[1])]))

    query = query.filter(Fact.shape.has(Shape.coordinates.any(Coordinates.quadrant_hash.in_(quadrants_coordinates))))
    return query


def filter_by_weight(query, weight):
    '''Filter facts by weight'''
    if weight:
        query = query.filter(Fact.weight <= weight)
    else:
        return query


def filter_by_ids(query, ids):
    '''Filter facts and return objects only with given ids'''
    if ids:
        facts_ids = ids
    else:
        return query

    query = query.filter(Fact.id.in_(facts_ids))
    return query

@hug.get('/facts',
         versions=1,
         examples=['start_date=12-22-1560&end_date=03-30-1570&topleft=56,78&bottomright=-22,10&weight=1',
                   'ids=[1,2,3,4]']
        )
def get_facts(start_date: hug.types.text=None,
          end_date: hug.types.text=None,
          topleft: list=None,
          bottomright: list=None,
          weight: int=None,
          ids: list=None
         ):
    '''API function for getting list of facts'''
    query = db.query(Fact)
    try:
        query = filter_by_time(query, start_date, end_date)
    except DateError as e:
        response = make_api_response(e.api_error(400))
        response.status_code = 400
        return response

    query = filter_by_geo(query, topleft, bottomright)
    query = filter_by_weight(query, weight)
    query = filter_by_ids(query, ids)
    result = query.all()

    serialized_result = []
    for fact in result:
        serialized = serialize(fact)
        serialized['start_date'] = fact.start_date.date.to_string()
        serialized['end_date'] = fact.end_date.date.to_string()
        serialized['type'] = {'name': fact.type.name, 'label': fact.type.label}
        serialized['shape'] = serialized['shape_id']
        serialized['description'] = serialized['description']
        serialized.pop('start_date_id')
        serialized.pop('end_date_id')
        serialized.pop('shape_id')
        serialized.pop('type_name')
        serialized.pop('text')
        serialized_result.append(serialized)

    return make_api_response(serialized_result)

@hug.get('/facts/{fact_id}')
def get_fact(fact_id):
    '''API function for getting single fact by id'''
    fact = db.query(Fact).get(fact_id)
    result = serialize(fact)

    result['start_date'] = fact.start_date.date.to_string()
    result['end_date'] = fact.end_date.date.to_string()
    result['type'] = {'name': fact.type.name, 'label': fact.type.label}
    result['shape'] = result['shape_id']
    # result['description'] = convert_wikitext(result['description'])
    # result['text'] = convert_wikitext(result['text'])
    # result.pop('text')
    result.pop('start_date_id')
    result.pop('end_date_id')
    result.pop('shape_id')
    result.pop('type_name')
    return make_api_response(result)
