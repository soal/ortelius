import hug

from ortelius.database import db
from ortelius.types.errors import NotFound, ServerError, BadRequest, MethodNotImplemented
from ortelius.models.Coordinates import Shape, Coordinates
from ortelius.models.Date import Date
from ortelius.middleware import filter_by_ids, filter_by_time, filter_by_weight, filter_quadrants, serialize, make_api_response, make_geojson_response


@hug.get('/shapes',
        versions=1,
        examples=['ids=[1,2,3,45,678]'])

def get_shapes(ids: list=None):
    query = db.query(Shape)

    query = filter_by_ids(query, Shape, ids)

    result = query.all()

    if not result:
        raise NotFound(resource_type='Shape')

    return make_geojson_response(result)


@hug.get('/shapes/{shape_id}')
def get_shape(shape_id):
    shape = db.query(Shape).get(shape_id)

    if not shape:
        raise NotFound(resource_type='Shape')

    return make_geojson_response(shape)
