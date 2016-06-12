import hug
import datetime

from ortelius.database import db
from ortelius.types.historical_date import HistoricalDate as hd
from ortelius.types.historical_date import DateError
from ortelius.types.errors import NotFound, ServerError, BadRequest, MethodNotImplemented
from ortelius.models.Hist_region import HistRegion, HistPlace
from ortelius.models.Coordinates import Shape, Coordinates
from ortelius.models.Date import Date
from ortelius.middleware import filter_by_ids, filter_by_time, filter_by_weight, filter_quadrants, serialize, make_api_response


@hug.get('/hist_regions',
         versions=1,
         examples=['start_date=12-22-1560&end_date=03-30-1570&topleft=56,78&bottomright=-22,10&weight=1',
                   'ids=[1,2,3,4]']
        )
def get_hist_regions(start_date: hug.types.text=None,
                     end_date: hug.types.text=None,
                     topleft: list=None,
                     bottomright: list=None,
                     weight: int=None,
                     ids: list=None
                    ):
    '''API function for getting list of historical regions'''

    query = db.query(HistRegion)

    query = filter_by_ids(query, HistRegion, ids)
    try:
        query = filter_by_time(query, HistRegion, start_date, end_date)
    except DateError:
        raise BadRequest()

    if topleft and bottomright:
        top_left = [float(x) for x in topleft]
        bottom_right = [float(x) for x in bottomright]
        quadrants_coordinates = filter_quadrants(top_left, bottom_right)

        if start_date:
            start = hd(start_date)
        else:
            start = hd(-50000101)
        if end_date:
            end = hd(end_date)
        else:
            end = hd(datetime.datetime.now())

        query = query.filter(HistRegion.shapes.any(Shape.start_date.has(Date.date >= start.to_int()),
                                                   Shape.end_date.has(Date.date <= end.to_int())))
        query = query.filter(HistRegion.shapes.any(Shape.coordinates.any(Coordinates.quadrant_hash.in_(quadrants_coordinates))))

    # query = filter_by_geo(query, HistRegion, topleft, bottomright)
    query = filter_by_weight(query, HistRegion, weight)
    result = query.all()

    return make_api_response(result)


@hug.get('/hist_regions/{hist_region_id}')
def get_hist_region(hist_region_id):
    '''API function for getting single historical region by id'''
    hist_region = db.query(HistRegion).get(hist_region_id)
    if hist_region:
        result = serialize(hist_region)
        result['facts']        = [fact.id for fact in hist_region.facts] if hist_region.facts else []
        result['personas']     = [persona.id for persona in hist_region.personas] if hist_region.personas else []
        result['shapes']       = [shape.id for shape in hist_region.shapes] if hist_region.shapes else []
        result['hist_places']  = [hist_place.id for hist_place in hist_region.hist_places] if hist_region.hist_places else []
        result['start_date']   = hist_region.start_date.date.to_string()
        result['end_date']     = hist_region.end_date.date.to_string()
        result['next_region']  = result['next_region_id']
        result['prev_region']  = result['prev_region_id']
        result['mark']         = hist_region.mark.id if hist_region.mark else None
        # result['description'] = convert_wikitext(result['description'])
        # result['text'] = convert_wikitext(result['text'])
        # result.pop('text')
        result.pop('start_date_id')
        result.pop('end_date_id')
        result.pop('next_region_id')
        result.pop('prev_region_id')
        return make_api_response(result)
    else:
        raise NotFound(resource_type='Process', identifiers={'id': hist_region_id})


@hug.post('/hist_regions')
def create_fact(data):
    '''API function for creating new historical region'''
    raise MethodNotImplemented(resource_type='Fact')


@hug.put('/hist_regions/{hist_region_id}')
def update_fact(hist_region_id, data):
    '''API function for updating existing historical region'''
    raise MethodNotImplemented(resource_type='Fact')


@hug.delete('/hist_regions/{hist_region_id}')
def delete_fact(hist_region_id):
    '''API function for deleting historical region'''
    raise MethodNotImplemented(resource_type='Fact')
