import hug

from ortelius.database import db
from ortelius.middleware import serialize, make_api_response
from ortelius.models.Element import ElementType


@hug.get('/')
def dicts():
    element_types = db.query(ElementType).all()
    result = {}
    result['element_types'] = [serialize(element_type) for element_type in element_types]
    return result
