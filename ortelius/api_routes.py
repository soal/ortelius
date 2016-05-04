from flask.ext.via.routers.default import Functional, Pluggable
from flask import send_file, request, abort
from ortelius.views.Facts_view import FactsView, TextView


def processes(id=[]):
    '''
        Get processes with optional search params.
        ?search - determinate search
        ?search&name - search by name
        ?from=12-22-1560 - search processes from this date
        ?to=03-30-1570 - search processes to this date
    '''

    if request.is_xhr:
        if id:
            pass
        else:
            return send_file('../test_data/%s.json', 'application/json') % id
    else:
        abort(404)


def georegions(id):
    '''Get georegion by name'''
    pass


def historical_regions(id=[]):
    '''Get historical georegion by name'''
    pass


def persons(id=[]):
    '''Get persons'''
    pass


def shapes(id=[]):
    '''Get shapes'''
    pass


def dicts():
    '''
    Return dicts:
    facts_type, historical_pers_types, georegions, quadrants???
    '''
    pass


def date(dates=[]):
    pass

routes = [
    Functional('/dicts', dicts),  # get all dicts for initializing client app
    Pluggable('/facts/<id>/text', TextView, 'text_view'),
    Pluggable('/facts/<id>', FactsView, 'facts_view'),  # get single fact by id
    Pluggable('/facts', FactsView, 'facts_view'),  # get single fact by id
    Functional('/processes', processes),  # get all processes or subset of processes
    Functional('/processes/<id>', processes),  # get single process
    Functional('/georegions/<id>', georegions),  # get georegion
    Functional('/historical-regions/<id>', historical_regions),  # get historical region
    Functional('/persons/<id>', persons),  # get person
    Functional('/shapes/<id>', shapes),  # get shapes
]
