from flask.views import MethodView
from ortelius.models.Date import Date
from ortelius.models.Fact import Fact
from flask import request, abort, jsonify, render_template_string
from ortelius.middleware import serialize

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
    http://handymap.com/api/facts?from=12-22-1560&to=03-30-1570&topleft=65.45,56.89&bottomright=69.45,50.89 - facts by dates in given quadrant
'''

acceptable_params = {'from': 'start_date',
                     'to': 'end_date',
                     'topleft': None,
                     'bottomright': None,
                     'search': None,
                     'name': 'name'}


# FIRST_DATE = Date.query.first()
# LAST_DATE = Date.query.last()


class FactsView(MethodView):
    """Facts view"""

    def get(self, id=None):
        if id:
            fact = Fact.query.get(id)
            if not fact:
                return jsonify(abort(404))
            result = serialize(Fact.query.get(id))

            result['start_date'] = fact.start_date.date.to_string()
            result['end_date'] = fact.end_date.date.to_string()
            result['type'] = { 'name': fact.type.name,   'label': fact.type.label }
            result['shape'] = result['shape_id']
            result.pop('start_date_id')
            result.pop('end_date_id')
            result.pop('shape_id')
            result.pop('type_name')
            return jsonify(result)

        else:
            query = Fact.query
            args_dict = request.args.to_dict
            if args_dict:
                pass
                # if args_dict['from'] or args_dict['to']:
                #     if args_dict['from']:
                #         start_date = args_dict['from']
                #     else:
                #         start_date = FIRST_DATE
                #     if args_dict['to']:
                #         pass
            else:
                pass



    def post(self):
        raise NotImplementedError()

    def put(self, id):
        raise NotImplementedError()

    def delete(self, id):
        raise NotImplementedError()
