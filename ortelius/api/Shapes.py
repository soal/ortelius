# import hug
#
# from ortelius.database import db
# from ortelius.types.errors import NotFound, ServerError, BadRequest, MethodNotImplemented
# from ortelius.models.Shape import Shape
# # from ortelius.middleware import filter_by_ids, make_geojson_response
#
#
# @hug.get('/shapes',
#         versions=1,
#         examples=['ids=[1,2,3,45,678]'])
#
# def get_shapes(ids: list=None):
#     if not ids:
#         raise BadRequest()
#
#     query = db.query(Shape)
#
#     query = filter_by_ids(query, Shape, ids)
#
#     result = query.all()
#
#     if not result:
#         raise NotFound(resource_type='Shape')
#
#     return make_geojson_response(result)
#
#
# @hug.get('/shapes/{shape_id}')
# def get_shape(shape_id):
#     shape = db.query(Shape).get(shape_id)
#
#     if not shape:
#         raise NotFound(resource_type='Shape')
#
#     return make_geojson_response(shape)
#
#
#
# @hug.post('/shapes')
# def create_shape(data):
#     '''API function for creating new shape'''
#     raise MethodNotImplemented(resource_type='Shape')
#
#
# @hug.put('/shapes/{shape_id}')
# def update_shape(shape_id, data):
#     '''API function for updating existing shape'''
#
#
# @hug.delete('/shapes/{shape_id}')
# def delete_shape(shape):
#     '''API function for deleting historical region'''
#     raise MethodNotImplemented(resource_type='Shape')
