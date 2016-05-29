import hug
import falcon


# FIXME: refactor.
class APIError(Exception):
    """Describe methods for api error"""

    def __init__(self, code=None, message=None):
        super(APIError, self).__init__()
        self.code = code
        self.message = message

    def api_error(self, code):
        self.code = code
        return {'code': self.code, 'message': self.message}

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
            self.description = '{0} identified by {1} not found.'.format(resource_type, identifiers)


class Forbidden(falcon.HTTPError):
    """Forbidden exception"""

    def __init__(self, resource_type=None, identifiers=None):
        super(Forbidden, self).__init__('403 Forbidden ')
        self.status = '403 Forbidden'
        self.title = 'Forbidden'
        if resource_type and identifiers:
            self.description = 'Requesting {0} identified by {1} not allowed.'.format(resource_type, identifiers)


class ServerError(falcon.HTTPError):
    """ServerError exception"""
    def __init__(self, resource_type=None, identifiers=None):
        super(ServerError, self).__init__('500 Internal Server Error')
        self.status = '500 Internal Server Error'
        self.title = 'Internal Server Error'
        if resource_type and identifiers:
            self.description = 'Requesting {0} identified by {1} casued server error.'.format(resource_type, identifiers)


class NotAuthorized(falcon.HTTPError):
    """Not Authorized exception"""

    def __init__(self, resource_type=None, identifiers=None):
        super(NotAuthorized, self).__init__('401 Not Authorized ')
        self.status = '401 Not Authorized'
        self.title = 'Not Authorized'
        if resource_type and identifiers:
            self.description = 'You are not authorized requesting {0} identified by {1}.'.format(resource_type, identifiers)


class MethodNotImplemented(falcon.HTTPError):
    """docstring for NotImplemented"""
    def __init__(self, resource_type=None):
        super(MethodNotImplemented, self).__init__('405 Method Not Allowed')
        self.status = '405 Method Not Allowed'
        self.title = 'Method not implemented'
        if resource_type:
            self.description = 'This method for {0} is not yet implemented.'.format(resource_type)
