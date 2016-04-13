from flask.ext.via.routers.default import Functional
from flask import render_template_string, send_file, request, abort

def index():
    return render_template_string('Welcome to Ortelius v1!')


def facts(id=None):
    '''
        Get facts with optional search params.
        ?from=12-22-1560 - search facts from this date
        ?to=03-30-1570 - search facts to this date

        ?topleft - coordinates of top left corner of the screen
        ?bottomright - coordinates bottom right corner of the screen

        ?search - determinate search
        ?search&name  - search by name
        ?search&date - search by date (use end date)

        Ex.:
        http://handymap.com/api/facts/36 - one fact by id
        http://handymap.com/api/facts?from=12-22-1560&to=03-30-1570&topleft:{x: 65.45, y: 56.89}&bottomright:{x: 69.45, y: 50.89} - facts by dates in given quadrant
    '''
    if request.is_xhr:
        if id: pass
        else: return send_file('../test_data/facts.json', 'application/json')
    else:
        abort(404)

def processes(id=[]):
    '''
        Get processes with optional search params.
        ?search - determinate search
        ?search&name - search by name
        ?from=12-22-1560 - search processes from this date
        ?to=03-30-1570 - search processes to this date
    '''

    if request.is_xhr:
        if id: pass
        else: return send_file('../test_data/%s.json', 'application/json') % id
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

    #API routes
    Functional('/api/dicts', dicts), #get all dicts for initializing client app
    Functional('/api/facts', facts), #get all facts or subset of facts
    Functional('/api/facts/<id>', facts), #get single fact by id
    Functional('/api/processes', processes), #get all processes or subset of processes
    Functional('/api/processes/<id>', processes), #get single process
    Functional('/api/georegions/<id>', georegions), #get georegion
    Functional('/api/historical-regions/<id>', historical_regions), #get historical region
    Functional('/api/persons/<id>', persons), #get peson
    Functional('/api/shapes/<id>', shapes), #get shapes
]
