import hug
from ortelius.types.errors import MethodNotImplemented

@hug.get('/')
def dicts():
    raise MethodNotImplemented()
