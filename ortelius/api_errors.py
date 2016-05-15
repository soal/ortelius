import hug

class BadRequest(hug.errors.HTTPBadRequest):
    '''Bad request exception'''
    def __init__(self):
        super(BadRequest, self).__init__()


class NotFound(hug.errors.HTTPNotFound):
    """Not found exception"""
    def __init__(self, resource_type=None, identifiers=None):
        super(NotFound, self).__init__()
        self.status = '404 Not found'
        self.title = 'Not Found'
        self.has_representation = True
        if resource_type and identifiers:
            self.description = '{0} identified by {1}, not found.'.format(resource_type, str(identifiers))
