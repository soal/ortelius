import hug

from ortelius.database import db
from ortelius.middleware import serialize, make_api_response
from ortelius.models.Element import ElementType


@hug.get('/')
def dicts():
    element_types = db.query(ElementType).all()

    result = {}
    result['element_types'] = [serialize(fact_type) for fact_type in element_types]

    return make_api_response(result)
