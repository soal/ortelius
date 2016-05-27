import hug

from ortelius.types.errors import NotFound, ServerError, NotAuthorized
from ortelius.models.Hist_region import HistRegion, HistPlace


hug.get('/hist_regions/{hrgeion_id}')
def get_hist_region():
    pass
