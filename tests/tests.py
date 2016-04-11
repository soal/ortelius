import unittest


class HandymapTestCase(unittest.TestCase):
    """HandymapTestCase - base class for calling unit tests on handymap"""
    def __init__(self, arg):
        super(HandymapTestCase, self).__init__()

    def setUp(self):
        self.app.config['TESTING'] = True
        self.app = self.app.test_client()

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
