import hug

from ortelius.database import db
from ortelius.middleware import serialize, make_api_response
from ortelius.types.errors import MethodNotImplemented
from ortelius.models.Fact import FactType
from ortelius.models.Process import ProcessType
from ortelius.models.Persona import PersType


@hug.get('/')
def dicts():
    fact_types = db.query(FactType).all()
    process_types = db.query(ProcessType).all()
    pers_types = db.query(PersType).all()

    result = {}
    result['fact_types'] = [serialize(fact_type) for fact_type in fact_types]
    result['process_types'] = [serialize(process_type) for process_type in process_types]
    result['pers_types'] = [serialize(pers_type) for pers_type in pers_types]

    return make_api_response(result)
