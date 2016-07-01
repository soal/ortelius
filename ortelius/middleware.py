import datetime
import geojson
from shapely.geometry import shape


from ortelius.types.historical_date import HistoricalDate as hd
from ortelius.models.Shape import Shape

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
    query = query.filter(model.start_date >= start.to_int(),
                         model.end_date <= end.to_int()
                        )
    return query


# def filter_by_geo(query, model, topleft, bottomright):
#     '''Filter facts by given quadrants in geocoordinates'''
#     if topleft and bottomright:
#         top_left = [float(x) for x in topleft]
#         bottom_right = [float(x) for x in bottomright]
#     else:
#         return query
#
#     # quadrants_coordinates = filter_quadrants(top_left, bottom_right)
#
#     if hasattr(model, 'shape'):
#         coordinates = 'point'
#         if model.shape.shape_type == 'Area':
#             coordinates = 'polygon'
#         if model.shape.shape_type == 'Route' or model.shape.shape_type == 'Movement':
#             coordinates = 'multipoint'
#         query = query.filter(model.shape.__getattribute__(coordinates)).contained('POLYGON(({1} {2},{3} {4},{5} {6},{7} {8}))'.format(top_left[0],
#                       top_left[1],
#
#                       top_left[0],
#                       bottom_right[1],
#
#                       bottom_right[0],
#                       bottom_right[1],
#
#                       bottom_right[0],
#                       top_left[1]))
#
#     if hasattr(model, 'shapes'):
#         query.filter(model.shapes.any(Shape.shape.coordinates).contained('POLYGON(({1} {2},{3} {4},{5} {6},{7} {8}))'.format(top_left[0],
#                       top_left[1],
#
#                       top_left[0],
#                       bottom_right[1],
#
#                       bottom_right[0],
#                       bottom_right[1],
#
#                       bottom_right[0],
#                       top_left[1])))
#     return query
#
#
# def filter_by_weight(query, model, weight):
#     '''Filter facts by weight'''
#     if weight:
#         query = query.filter(model.weight <= weight)
#     return query
#
#
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

def convert_to_ewkt(coordinates):
    return 'SRID=4326;' + shape(coordinates).wkt

def make_geojson_feature(data):
    return geojson.Feature(id=data.id,
                           geometry=geojson.loads(data.coordinates[0]),
                           properties={
                                'start_date': data.start_date.to_string(),
                                'end_date': data.end_date.to_string(),
                                'stroke': data.stroke_color,
                                'stroke-opacity': data.stroke_opacity,
                                'fill': data.fill_color,
                                'fill-opacity': data.fill_opacity
                           }
                          )

def make_geojson_response(data):
    if isinstance(data, list):
        return geojson.FeatureCollection([make_geojson_feature(shape) for shape in data])
    else:
        return make_geojson_feature(data)
