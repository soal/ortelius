import hug

from ortelius.types.errors import NotFound, ServerError, NotAuthorized, MethodNotImplemented
from ortelius.models.Hist_region import HistRegion, HistPlace


hug.get('/hist_regions/{hist_region_id}')
def get_hist_region(hist_region_id):
    raise MethodNotImplemented(resource_type='Historical region')
