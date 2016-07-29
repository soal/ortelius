'''
Get elements with optional search params.
?start_date=12-22-1560 — search facts from this date
?end_date=03-30-1570 — search facts to this date

?topleft — coordinates of top left corner of the screen
?bottomright — coordinates bottom right corner of the screen
?ids — list of elements ids

Ex.:
http://handymap.com/api/elements/36 - one fact by id
http://handymap.com/api/elements?ids=1,5,23,67 - list of elements by given ids
http://handymap.com/api/elements?start_date=12-22-1560&end_date=03-30-1570&topleft=65.45,56.89&bottomright=69.45,50.89 - facts by dates in given quadrant
'''

import hug
import datetime

from ortelius.types.errors import NotFound, BadRequest, MethodNotImplemented
from ortelius.types.historical_date import HistoricalDate as hd
from ortelius.types.historical_date import DateError
from ortelius.database import db
from ortelius.models.Element import Element
from ortelius.middleware import serialize, make_api_response, filter_by_ids
# from ortelius.middleware import serialize, make_api_response, filter_by_ids, filter_by_time, filter_by_weight


'''
Get processes with optional search params.
?start_date=12-22-1560 — search facts from this date
?end_date=03-30-1570 — search facts to this date

?topleft — coordinates of top left corner of the screen
?bottomright — coordinates bottom right corner of the screen
?ids — list of processes ids

Ex.:
http://handymap.com/api/elements/36 - one fact by id
http://handymap.com/api/elements?ids=1,5,23,67 - list of elements by given ids
http://handymap.com/api/elements?start_date=12-22-1560&end_date=03-30-1570&topleft=65.45,56.89&bottomright=69.45,50.89 - elements by dates in given quadrant
'''


@hug.get('/',
         examples=['start_date=12-22-1560&end_date=03-30-1570&weight=1',
                   'ids=1,2,3,4']
        )
def get_elements(start_date: hug.types.text=None,
                  end_date: hug.types.text=None,
                  weight: int=None,
                  ids: list=None):
    # raise MethodNotImplemented(resource_type='Element')
    print(ids)
    if not ids or not all(id.isdigit() for id in ids):
        raise BadRequest(info="No ids")
    query = db.query(Element)
    query = filter_by_ids(query, Element, ids)
    result = query.all()
    if not result: # FIXME: what if we could find something, but not all?
        raise NotFound(resource_type='Element', identifiers=ids)

    serialized = []
    for element in result:
        serialized_element = serialize(element)
        serialized.append(serialized_element)

    return make_api_response(serialized)

@hug.get('/{element_id}')
def get_element(element_id: int):
    query = db.query(Element)
    query = query.filter(Element.id == element_id)
    result = query.first()
    if not result:
        raise NotFound(resource_type='Element', identifiers=element_id)
    return make_api_response(serialize(result))

@hug.post('/')
def create_element(**data):
    '''API function for creating new fact'''
    import inspect
    initParms = inspect.signature(Element.__init__).parameters.values()
    validArgs = {parm.name for parm in initParms if parm.name != 'self'}
    requiredArgs = {parm.name for parm in initParms if parm.name != 'self' and parm.default == inspect._empty}
    args = set(data.keys())
    if not args.issubset(validArgs) or not requiredArgs.issubset(args):
        invalidArgs = args - validArgs
        missingArgs = requiredArgs - args
        raise BadRequest(missingArgs, invalidArgs, info="Parameters validation failed")
    try:
        element=Element(**data)
    except:
        raise BadRequest(info="Model construction failed")
    try:
        db.session.add(element)
        db.session.commit()
    except: # IntegrityError
        db.session.rollback()
        raise BadRequest(info="Database transaction failed")
    return make_api_response('OK')


@hug.put('/elements/{element_id}')
def update_element(element_id, data):
    '''API function for updating existing process'''
    raise MethodNotImplemented(resource_type='Element')


@hug.delete('/{element_id}')
def delete_element(element_id: int):
    '''API function for deleting process'''
    query = db.query(Element)
    query = query.filter(Element.id == element_id)
    result = query.first() # query.get
    if not result:
        raise NotFound(resource_type='Element', identifiers=element_id)
    db.session.delete(result)
    # db.session.remove(result)
    db.session.commit()
    return make_api_response('OK')

#     '''API function for getting list of processes'''
#     query = db.query(Process)
#     query = filter_by_ids(query, Process, ids)
#     try:
#         query = filter_by_time(query, Process, start_date, end_date)
#     except DateError:
#         raise BadRequest()
#
#     query = filter_by_weight(query, Process, weight)
#     result = query.all()
#
#     if not result:
#         raise NotFound()
#
#     serialized_result = []
#
#     for process in result:
#         serialized = serialize(process)
#         serialized['facts']        = [fact.id for fact in process.facts] if process.facts else []
#         serialized['subprocesses'] = [subprocess.id for subprocess in process.subprocesses] if process.subprocesses else []
#         serialized['personas']     = [persona.id for persona in process.personas] if process.personas else []
#         serialized['shapes']       = [shape.id for shape in process.shapes] if process.shapes else []
#         serialized['hist_regions'] = [hist_region.id for hist_region in process.hist_regions] if process.hist_regions else []
#         serialized['hist_places']  = [hist_place.id for hist_place in process.hist_places] if process.hist_places else []
#         serialized['start_date']   = process.start_date.date.to_string()
#         serialized['end_date']     = process.end_date.date.to_string()
#         serialized['type']         = {'name': process.type.name, 'label': process.type.label}
#         serialized.pop('start_date_id')
#         serialized.pop('end_date_id')
#         serialized.pop('type_name')
#         serialized.pop('text')
#         serialized_result.append(serialized)
#
#     return make_api_response(serialized_result)
#
#
# @hug.get('/elements/{process_id}')
# def get_process(process_id):
#     '''API function for getting single process by id'''
#     process = db.query(Process).get(process_id)
#     if process:
#         result = serialize(process)
#         result['facts']        = [fact.id for fact in process.facts] if process.facts else []
#         result['subprocesses'] = [subprocess.id for subprocess in process.subprocesses] if process.subprocesses else []
#         result['personas']     = [persona.id for persona in process.personas] if process.personas else []
#         result['shapes']       = [shape.id for shape in process.shapes] if process.shapes else []
#         result['hist_regions'] = [hist_region.id for hist_region in process.hist_regions] if process.hist_regions else []
#         result['hist_places']  = [hist_place.id for hist_place in process.hist_places] if process.hist_places else []
#         result['start_date']   = process.start_date.date.to_string()
#         result['end_date']     = process.end_date.date.to_string()
#         result['type']         = {'name': process.type.name, 'label': process.type.label}
#         # result['description'] = convert_wikitext(result['description'])
#         # result['text'] = convert_wikitext(result['text'])
#         # result.pop('text')
#         result.pop('start_date_id')
#         result.pop('end_date_id')
#         result.pop('type_name')
#         return make_api_response(result)
#     else:
#         raise NotFound(resource_type='Element', identifiers={'id': element_id})
