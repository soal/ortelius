import hug

from ortelius.database import db
from ortelius.types.errors import NotFound, ServerError, BadRequest, MethodNotImplemented
from ortelius.models.Coordinates import Shape
# from ortelius.models.Date import Date
from ortelius.middleware import filter_by_ids, make_geojson_response


@hug.get('/shapes',
        versions=1,
        examples=['ids=[1,2,3,45,678]'])

def get_shapes(ids: list=None):
    if not ids:
        raise BadRequest()

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
