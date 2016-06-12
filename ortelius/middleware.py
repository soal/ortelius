import datetime
# from json import dumps

from ortelius.types.historical_date import HistoricalDate as hd
from ortelius.models.Date import Date
from ortelius.models.Coordinates import Quadrant, Shape, Coordinates

def serialize(sqlalchemy_obj):
    serialized = {}
    for field in sqlalchemy_obj._sa_class_manager.mapper.mapped_table.columns.keys():
        serialized[field] = sqlalchemy_obj.__getattribute__(field)
    return serialized


# def convert_wikitext(wikitext):
#     from smc import mw
#     from lxml import etree, html
#     from lxml.html import clean
#
#     ast = mw.MediaWiki(wikitext).as_string()
#     cleaner = clean.Cleaner(remove_tags=['html', 'body', 'pre'], remove_unknown_tags=False)
#     cleaned = cleaner.clean_html(html.fromstring(ast))
#
#     return etree.tounicode(cleaned)
#
#
def filter_by_time(query, model, start_date, end_date):
    '''Filter facts by date'''
    if start_date:
        start = hd(start_date)
    else:
        start = hd(-50000101)
    if end_date:
        end = hd(end_date)
    else:
        end = hd(datetime.datetime.now())
    query = query.filter(model.start_date.has(Date.date >= start.to_int()),
                         model.end_date.has(Date.date <= end.to_int())
                        )
    return query


def filter_quadrants(top_left, bottom_right):
    quadrants_coordinates = []
    for c in Quadrant.quadrants:
        if c[0] >= top_left[0] - 4 and c[0] <= bottom_right[0] and c[1] >= top_left[1]-4 and c[1] <= bottom_right[1]:
            quadrants_coordinates.append(','.join([str(c[0]), str(c[1])]))

    return quadrants_coordinates

def filter_by_geo(query, model, topleft, bottomright):
    '''Filter facts by given quadrants in geocoordinates'''
    if topleft and bottomright:
        top_left = [float(x) for x in topleft]
        bottom_right = [float(x) for x in bottomright]
    else:
        return query

    quadrants_coordinates = filter_quadrants(top_left, bottom_right)

    if hasattr(model, 'shape'):
        query = query.filter(model.shape.has(Shape.coordinates.any(Coordinates.quadrant_hash.in_(quadrants_coordinates))))

    return query


def filter_by_weight(query, model, weight):
    '''Filter facts by weight'''
    if weight:
        query = query.filter(model.weight <= weight)
    return query


def filter_by_ids(query, model, ids):
    '''Filter facts and return objects only with given ids'''
    if ids:
        object_ids = ids
    else:
        return query

    query = query.filter(model.id.in_(object_ids))
    return query


def make_api_response(data, pages=None, total=None):
    return {
        'meta': {
            'total': len(data) if isinstance(data, list) or isinstance(data, tuple) or isinstance(data, dict) else None,
            'pages': pages,
        },
        'data': data
    }
