import hug
import datetime

from ortelius.database import db
from ortelius.types.historical_date import HistoricalDate as hd
from ortelius.types.historical_date import DateError
from ortelius.types.errors import NotFound, ServerError, BadRequest, MethodNotImplemented
from ortelius.models.Hist_region import HistRegion, HistPlace
from ortelius.middleware import filter_by_geo, filter_by_ids, filter_by_time, filter_by_weight, serialize, make_api_response


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

    raise MethodNotImplemented(resource_type='Historical region')


@hug.get('/hist_regions/{hist_region_id}')
def get_hist_region(hist_region_id):
    '''API function for getting single historical region by id'''
    raise MethodNotImplemented(resource_type='Historical region')


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
