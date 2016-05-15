import hug
import falcon


# FIXME: reactor.
class APIError(Exception):
    """Describe methods for api error"""

    def __init__(self, code=None, message=None):
        super(APIError, self).__init__()
        self.code = code
        self.message = message

        def api_error(self, code):
            self.code = code
            return {'code': self.code, 'message': self.message }

        def __repr__(self):
            return 'APIError: code %s, %s' % (self.code, self.message)


class BadRequest(falcon.HTTPError):
    '''Bad request exception'''

    def __init__(self):
        super(BadRequest, self).__init__(status='400 BadRequest')


class NotFound(falcon.HTTPError):
    """Not found exception"""

    def __init__(self, resource_type=None, identifiers=None):
        super(NotFound, self).__init__('404 NotFound')
        self.status = '404 Not found'
        self.title = 'Not Found'
        if resource_type and identifiers:
            self.description = '{0} identified by {1}, not found.'.format(resource_type, identifiers)
