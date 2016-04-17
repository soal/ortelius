from flask.ext.via.routers.default import Functional, Pluggable
from flask import render_template_string, send_file, request, abort
from ortelius.views.facts import FactsView


def index():
    return render_template_string('Welcome to Ortelius v1!')


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
    Functional('/', index),

    # API routes
    Functional('/api/dicts', dicts),  # get all dicts for initializing client app
    Pluggable('/api/facts/<id>', FactsView, 'facts_view'),  # get single fact by id
    Pluggable('/api/facts', FactsView, 'facts_view'),  # get single fact by id
    Functional('/api/processes', processes),  # get all processes or subset of processes
    Functional('/api/processes/<id>', processes),  # get single process
    Functional('/api/georegions/<id>', georegions),  # get georegion
    Functional('/api/historical-regions/<id>', historical_regions),  # get historical region
    Functional('/api/persons/<id>', persons),  # get person
    Functional('/api/shapes/<id>', shapes),  # get shapes
]
