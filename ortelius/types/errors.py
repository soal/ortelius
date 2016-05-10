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
