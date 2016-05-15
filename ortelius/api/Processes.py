import hug
import datetime

from ortelius.database import db
from ortelius.models.Date import Date
from ortelius.models.Process import Process, ProcessType
from ortelius.middleware import serialize, make_api_response


def filter_by_time(query, start_date, end_date):
    pass

def fulter_by_ids(query, ids):
    pass


@hug.get('/processes',
         examples=['start_date=12-22-1560&end_date=03-30-1570weight=1',
                   'ids=[1,2,3,4]']
        )
def get_processes():
    '''API function for getting list of processes'''
    return 'Hello from processes!'


@hug.get('/processes/{process_id}')
def get_process(process_id):
    '''API function for getting single process by id'''
    process = db.query(Process).get(process_id)
    if process:
        result = serialize(process)

        result['start_date'] = process.start_date.date.to_string()
        result['end_date'] = process.end_date.date.to_string()
        result['type'] = {'name': process.type.name, 'label': process.type.label}
        # result['description'] = convert_wikitext(result['description'])
        # result['text'] = convert_wikitext(result['text'])
        # result.pop('text')
        result.pop('start_date_id')
        result.pop('end_date_id')
        result.pop('type_name')
        return make_api_response(result)
    else:
        raise hug.errors.HTTPNotFound()
